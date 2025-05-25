// src/api/home.js
import request from './axios'; // 你的 Axios 實例

const BASE_IMAGE_URL = 'http://127.0.0.1:8000';
console.log('home.js: Script loaded. BASE_IMAGE_URL =', BASE_IMAGE_URL);

// 使用上一輪提供的極簡版 formatSalaryMinimal 和 transformJobDataMinimal, transformCompanyDataMinimal
function formatSalaryMinimal(apiJobData) {
  const { salary_type, salary_min, salary_max, salary_number } = apiJobData;
  let resultS = '薪資面議'; // 預設值
  if (salary_type && salary_min && salary_max && String(salary_min) !== '0' && String(salary_max) !== '0') {
    resultS = `${salary_type} ${salary_min}~${salary_max} 元`; // 稍微調整格式
  } else if (salary_type && salary_min && String(salary_min) !== '0') {
    resultS = `${salary_type} ${salary_min} 元以上`;
  } else if (salary_type === '時薪' && salary_number) {
    resultS = `${salary_type} ${String(salary_number)} 元`;
  } else if (salary_type && (salary_type.includes('面議') || (salary_type === '月薪' && !salary_min && !salary_max && !salary_number))) {
    resultS = salary_type.includes('面議') ? salary_type : `${salary_type} 面議`;
  } else if (salary_type) {
    resultS = salary_type;
  }
  // console.log(`[formatSalaryMinimal] For ID ${apiJobData.id}: ${resultS}`);
  return resultS;
}

function transformJobDataMinimal(apiJob) {
  // console.log(`[transformJobDataMinimal] Input for ID ${apiJob ? apiJob.id : 'N/A'}:`, apiJob ? JSON.parse(JSON.stringify(apiJob)) : 'null/undefined');
  if (!apiJob || typeof apiJob !== 'object' || typeof apiJob.id === 'undefined') {
    console.error('[transformJobDataMinimal] Invalid or missing ID in apiJob:', apiJob);
    return null;
  }
  const transformed = {
    id: apiJob.id,
    title: apiJob.title || '未知標題',
    image: apiJob.company_logo ? `${BASE_IMAGE_URL}${apiJob.company_logo}` : '/img/placeholder-job.png',
    company: apiJob.company && apiJob.company.name ? apiJob.company.name : '未知公司',
    salary: formatSalaryMinimal(apiJob),
    originalData: apiJob
  };
  // console.log(`[transformJobDataMinimal] Output for ID ${apiJob.id}:`, JSON.parse(JSON.stringify(transformed)));
  return transformed;
}

function transformCompanyDataMinimal(companyInfo) {
  // console.log('[transformCompanyDataMinimal] Input:', companyInfo);
  if (!companyInfo || typeof companyInfo !== 'object') return null;
  const transformed = {
    id: companyInfo.id || companyInfo.name,
    name: companyInfo.name || '未知企業',
    image: companyInfo.logo ? `${BASE_IMAGE_URL}${companyInfo.logo}` : '/img/placeholder-company.png',
  };
  // console.log('[transformCompanyDataMinimal] Output:', transformed);
  return transformed;
}

// fetchGenericJobsList 現在直接處理從攔截器返回的數據
async function fetchGenericJobsList(endpointName, apiParams = {}) {
  try {
// 正確的行：
    const backendParams = { page_size: apiParams.limit ? Math.max(apiParams.limit * 2, 20) : 20 };
    console.log(`[${endpointName}] Attempting to fetch from /api/jobs/ with params:`, backendParams);

    // 'responseData' 現在就是攔截器返回的 actual data (通常是陣列或物件)
    const responseData = await request({ url: '/api/jobs/', method: 'get', params: backendParams });
    console.log(`[${endpointName}] Data received directly from request (due to interceptor):`, responseData);

    // 現在 responseData 就是我們期望的數據陣列 (或者需要從中提取 .results 的物件)
    // 根據你的 API (/api/jobs/) 直接返回陣列的行為：
    const dataArray = Array.isArray(responseData) ? responseData : [];
    console.log(`[${endpointName}] Final dataArray (length ${dataArray.length}):`, JSON.parse(JSON.stringify(dataArray)));

    if (!dataArray.length) {
        console.warn(`/api/jobs/ for [${endpointName}] resulted in empty dataArray.`);
        return [];
    }

    const transformedJobs = dataArray.map(transformJobDataMinimal).filter(job => job !== null);
    console.log(`[${endpointName}] Transformed jobs (length ${transformedJobs.length}):`, JSON.parse(JSON.stringify(transformedJobs)));
    
    return transformedJobs.slice(0, apiParams.limit || 10);

  } catch (error) {
    console.error(`Error in fetchGenericJobsList for [${endpointName}]:`, error.message, error);
    if (error.response) { // 如果錯誤物件仍然是 Axios 錯誤物件 (例如攔截器中的 reject)
        console.error(`[${endpointName}] Axios error details:`, error.response.data, error.response.status);
    }
    throw error; // 重新拋出，讓 Home.vue 可以捕獲並設置 UI 狀態
  }
}

// --- API 函數 (getRecommendedJobs, getHotJobs, etc.) 保持不變 ---
export async function getRecommendedJobs(params = { limit: 10 }) {
  return fetchGenericJobsList('Recommended', params);
}
export async function getHotJobs(params = { limit: 10 }) {
  return fetchGenericJobsList('Hot', params);
}
export async function getLatestJobs(params = { limit: 10 }) {
  return fetchGenericJobsList('Latest (Unsorted)', params);
}

export async function getTopCompanies(params = { limit: 10 }) {
  const allJobsForCompanies = await fetchGenericJobsList('JobsForCompaniesExtraction', { limit: 100 }); // limit 設大一點以獲取足夠公司樣本
  const companiesMap = new Map();
  allJobsForCompanies.forEach(job => {
    if (job && job.originalData && job.originalData.company && job.originalData.company.name) {
      const companyName = job.originalData.company.name;
      const companyLogo = job.originalData.company_logo;
      const companyId = job.originalData.company.id;
      if (companyName && !companiesMap.has(companyName)) {
        companiesMap.set(companyName, { id: companyId || companyName, name: companyName, logo: companyLogo });
      }
    } else {
      console.warn('[getTopCompanies] Skipping job due to missing data in originalData for company extraction:', job ? JSON.stringify(job.originalData) : 'job is null/undefined');
    }
  });
  const uniqueCompanies = Array.from(companiesMap.values());
  const transformedCompanies = uniqueCompanies.map(transformCompanyDataMinimal).filter(c => c !== null);
  return transformedCompanies.slice(0, params.limit || 10);
}

// getJobDetail 也需要相應調整
export async function getJobDetail(jobId) {
  try {
    console.log(`Workspaceing job detail for ${jobId}`);
    // 'jobData' 已經是攔截器處理後的 response.data
    const jobData = await request({ url: `/api/jobs/${jobId}/`, method: 'get' });
    if (jobData) { // 直接檢查 jobData
      return transformJobDataMinimal(jobData);
    }
    console.warn(`No data returned for job detail ${jobId}`);
    return null;
  } catch (error) {
    console.error(`Error fetching job detail for ${jobId}:`, error.message, error);
    if (error.response) {
        console.error(`[getJobDetail] Axios error details:`, error.response.data, error.response.status);
    }
    throw error;
  }
}

export async function searchJobsApi(searchCriteria = {}) {
  // searchCriteria 預期是一個物件，例如從 SearchResult.vue 傳來的：
  // { keyword: '工程師', positions: ['position1', 'position2'], regions: ['台北市', '新北市'] }
  const { keyword, positions, regions } = searchCriteria;

  try {
    // 1. 準備要發送給後端的參數
    const backendParams = {};

    if (keyword && keyword.trim() !== '') {
      backendParams.keyword = keyword.trim();
    }
    if (positions && positions.length > 0) {
      backendParams.positions = positions.join(',');
    }
    if (regions && regions.length > 0) {
      backendParams.regions = regions.join(',');
    }

    // 2. 定義您的搜尋 API 端點 (Endpoint)
    //    - 情況 A: 可能是您現有的 /api/jobs/ 端點，通過不同的查詢參數來實現搜尋。
    //    - 情況 B: 或者是一個專門用於搜尋的端點，例如 /api/jobs/search/。
    //    << CONFIRM >> 請與後端確認並替換為您真實的搜尋 API 端點。
    const searchEndpoint = '/api/jobs/';

    console.log(`[searchJobsApi] 準備請求 API: ${searchEndpoint} 使用參數:`, JSON.parse(JSON.stringify(backendParams)));

    // 3. 發送 API 請求
    //    'responseData' 應該是您的 Axios 攔截器處理後直接返回的數據部分 (根據您 fetchGenericJobsList 中的註釋)
    const responseData = await request({
      url: searchEndpoint,
      method: 'get', // 搜尋請求通常使用 GET 方法
      params: backendParams // axios 會自動將 params 物件轉換為 URL query string
    });

    console.log(`[searchJobsApi] API 直接回傳數據 (可能經攔截器處理):`, responseData);

    // 4. 處理 API 回應並轉換數據
    //    您需要根據後端 API 回傳的實際數據結構來調整這部分。
    let jobsArray = [];
    let paginationInfo = null; // 用於儲存可能的分頁信息

    if (Array.isArray(responseData)) {
      // 情況 1: API 直接回傳職缺陣列
      jobsArray = responseData;
    } else if (responseData && Array.isArray(responseData.results)) {
      // 情況 2: API 回傳物件，職缺在 'results' 鍵下 (常見於 Django Rest Framework 分頁)
      jobsArray = responseData.results;
      paginationInfo = {
        count: responseData.count,
        next: responseData.next,
        previous: responseData.previous
        // ... 您 API 可能提供的其他分頁字段
      };
    } else if (responseData && Array.isArray(responseData.data)) {
      // 情況 3: API 回傳物件，職缺在 'data' 鍵下 (另一種常見的包裹格式)
      jobsArray = responseData.data;
      if (responseData.pagination) paginationInfo = responseData.pagination; // 例如 { currentPage, totalPages, ... }
    } else if (responseData === null || (typeof responseData === 'object' && Object.keys(responseData).length === 0 && !Array.isArray(responseData))) {
      // 情況 4: API 回傳空物件或 null
      console.warn(`[searchJobsApi] API 回傳為空物件或 null。`);
      jobsArray = [];
    } else {
      // 情況 5: 未知的回傳格式
      console.warn(`[searchJobsApi] API 回傳格式非預期 (不是陣列，也沒有 .results 或 .data 陣列)。收到的數據:`, responseData);
      jobsArray = []; // 預設為空陣列以避免錯誤
    }

    if (!jobsArray.length) {
      console.warn(`[searchJobsApi] 搜尋參數 ${JSON.stringify(backendParams)} 沒有返回任何職缺數據 (jobsArray 為空)。`);
      return { jobs: [], pagination: paginationInfo }; // 始終返回一致的結構
    }

    // 5. 使用您已有的 transformJobDataMinimal 函數轉換數據
    const transformedJobs = jobsArray.map(transformJobDataMinimal).filter(job => job !== null);
    console.log(`[searchJobsApi] 轉換後的職缺 (數量 ${transformedJobs.length}):`, JSON.parse(JSON.stringify(transformedJobs)));

    return {
      jobs: transformedJobs,
      pagination: paginationInfo // 也回傳分頁信息，供 SearchResult.vue 未來可能的分頁功能使用
    };

  } catch (error) {
    console.error(`[searchJobsApi] 請求 API 時發生錯誤:`, error.message, error);
    if (error.response) {
      console.error(`[searchJobsApi] Axios 錯誤詳情:`, error.response.data, error.response.status);
    }
    throw error; // 重新拋出錯誤，讓 SearchResult.vue 組件可以捕獲並處理 UI
  }
}


// likeJob 和 unlikeJob 不需要大的改動，因為它們的返回值我們通常只關心是否成功，
// 攔截器不影響它們拋出錯誤的行為。
export async function likeJob(jobId) {
  try {
    // 攔截器可能會返回 response.data (例如一個成功訊息物件)，或者如果 API 沒有返回內容，則可能是 undefined
    const resultData = await request({ url: `/api/jobs/${jobId}/like/`, method: 'post' });
    console.log(`Liking job ${jobId} - API response data:`, resultData);
    return resultData; // 或 return true;
  } catch (error) {
    console.error(`Error liking job ${jobId}:`, error.message, error);
    if (error.response) {
        console.error(`[likeJob] Axios error details:`, error.response.data, error.response.status);
    }
    throw error;
  }
}

export async function unlikeJob(jobId) {
  try {
    const resultData = await request({ url: `/api/jobs/${jobId}/unlike/`, method: 'post' });
    console.log(`Unliking job ${jobId} - API response data:`, resultData);
    return resultData; // 或 return true;
  } catch (error) {
    console.error(`Error unliking job ${jobId}:`, error.message, error);
    if (error.response) {
        console.error(`[unlikeJob] Axios error details:`, error.response.data, error.response.status);
    }
    throw error;
  }
}