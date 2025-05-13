<template>
    <div class="middle-content"></div>
</template>

<script>
export default {
    name: 'Company'
}
</script>

<style scoped>
.middle-content {
    width: 100%;
    max-width: 850px;
    position: fixed; /* 固定位置 */
    margin-top: -4px;
    padding: 16px;
    height: calc(100vh - 72px);
    background-color: #383333;
    border-radius: 10px;
    color: white;
    box-sizing: border-box;
    overflow-x: hidden;
    overflow-y: auto;
}
</style>