from django.conf import settings

class PermissionsPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # 构建权限策略头
        policy_strings = []
        for feature, values in getattr(settings, 'PERMISSIONS_POLICY', {}).items():
            if not values:
                policy_strings.append(f"{feature}=()")
            else:
                policy_strings.append(f"{feature}=({' '.join(values)})")
        
        if policy_strings:
            response['Permissions-Policy'] = ', '.join(policy_strings)
        
        return response 