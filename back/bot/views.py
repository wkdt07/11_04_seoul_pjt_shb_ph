# import openai
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.conf import settings

# def chat(request):
#     if request.method == "POST":
#         user_message = request.POST.get('message')
#         if user_message:
#             openai.api_key = settings.OPENAI_API_KEY

#             # 대화 기록 초기화
#             messages = [
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": user_message}
#             ]

#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=messages
#             )
#             ai_message = response.choices[0].message['content']
#             return JsonResponse({'message': ai_message})
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return render(request, 'chat.html')
# import openai
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.conf import settings
# from .models import Deposit, Saving
# from .serializers import SavingSerializer, DepositSerializer

# def extract_criteria(user_input):
#     openai.api_key = settings.OPENAI_API_KEY
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Extract criteria and threshold from the following user input: '{user_input}'. Output in JSON format.",
#         max_tokens=50
#     )
#     criteria_data = response.choices[0].text.strip()
#     return json.loads(criteria_data)

# def recommend_financial_products(request): #알고리즘
#     if request.method == "POST":
#         user_message = request.POST.get('message')
        
#         if user_message:
#             # 사용자의 입력을 해석하여 기준 추출
#             criteria_data = extract_criteria(user_message)
#             criteria = criteria_data.get('criteria', 'save_trm')
#             threshold = criteria_data.get('threshold', 12)
            
#             # 기준에 따라 데이터 필터링
#             filtered_savings = Saving.objects.filter(options__save_trm__lte=threshold)
#             filtered_deposits = Deposit.objects.filter(options__save_trm__lte=threshold)
            
#             # 시리얼라이징
#             saving_serializer = SavingSerializer(filtered_savings, many=True)
#             deposit_serializer = DepositSerializer(filtered_deposits, many=True)
            
#             # OpenAI API 호출을 위한 메시지 생성
#             messages = [
#                 {"role": "system", "content": "You are an AI that provides financial product recommendations."},
#                 {"role": "user", "content": f"Recommend financial products with a {criteria} of {threshold} or less."},
#                 {"role": "assistant", "content": "Here are some options:"}, 
#                 # assistant는 모델이 사용자에게 응답할 때 활용. 모든 모델의 응답 메세지는 이 역할로 지정되어야 함
#                 {"role": "assistant", "content": f"Savings: {saving_serializer.data}"},
#                 {"role": "assistant", "content": f"Deposits: {deposit_serializer.data}"}
#             ]
            
#             '''
#             assistant 역할의 기능과 중요성
#                 1.모델의 응답:

#                 assistant 역할은 모델이 사용자에게 응답할 때 사용됩니다.
#                 모든 모델의 응답 메시지는 이 역할로 지정되어야 합니다.
                
#                 2. 대화의 연속성:

#                     assistant 역할을 사용하여 이전 대화의 문맥을 유지할 수 있습니다.
#                     이는 대화의 자연스러움을 유지하고, 모델이 일관된 응답을 생성하도록 돕습니다.
                
#                 3. 대화 기록 관리:

#                 assistant 역할을 사용하여 모델의 응답을 기록하고, 이후 대화에서 참조할 수 있습니다.
#                 예를 들어, 이전 대화 내용을 바탕으로 더 정확하고 문맥에 맞는 응답을 생성할 수 있습니다.
#             '''
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=messages
#             )
            
#             ai_message = response.choices[0].message['content']
#             return JsonResponse({'recommendation': ai_message})
        
#         return JsonResponse({'error': 'No message provided'}, status=400)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=400)



# ## IsAuthenticated를 통과한다면 recommend로(아니면 user 모델의 옵션(fav_place)이 null 이 아니라면), 아니면 단순 챗봇으로 사용할 수 있도록(근데 null이면 고를 수 있는 페이지로 넘기는 것도 방법이겠다)


# # 1. 만약 null이면 fav_place 기능을 제외하고 쓰기
# # 2. 만약 null이 아니라면 -> 이걸 위주로 설명해주기


# # 부동산 평균가격, 위치 등을 읽어온 다음 데이터들과 엮으면 되겠다(헤당 지역을 선택한 사람의 수는 RealEstate모델에서 filter 한 다음 User의 갯수 count 하면 됨)



import openai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Answer
from compare.models import Deposit, Saving
from compare.serializer import SavingSerializer, DepositSerializer
from accounts.models import User  # User 모델 임포트
import requests
import openai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def get_fav_place_products(region_id):
    # 해당 지역 ID를 가진 사용자들 가져오기
    users_in_place = User.objects.filter(fav_place=region_id)
    
    # 해당 사용자들이 가입한 금융 상품들 가져오기
    user_deposits = Deposit.objects.filter(user__in=users_in_place)
    user_savings = Saving.objects.filter(user__in=users_in_place)
    
    # 가장 많이 가입된 상위 5개 상품 가져오기
    top_deposits = list(user_deposits.values('name').annotate(count=Count('name')).order_by('-count')[:5])
    top_savings = list(user_savings.values('name').annotate(count=Count('name')).order_by('-count')[:5])
    
    # 추천 항목이 5개가 안 되는 경우 처리
    while len(top_deposits) < 5:
        top_deposits.append({'name': 'No more deposits available', 'count': 0})
        
    while len(top_savings) < 5:
        top_savings.append({'name': 'No more savings available', 'count': 0})

    return top_deposits, top_savings


def get_real_estate_id(region):
    url = f"{settings.BASE_URL}/real_estate/recent/{region}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('id')
    return None


# 이거 지워야 한다. 
@csrf_exempt
@login_required
def chat(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '사용자가 인증되지 않았습니다.'}, status=403)

    if request.method == "POST":
        user_message = request.POST.get('message')
        if not user_message:
            return JsonResponse({'error': '메시지가 제공되지 않았습니다.'}, status=400)
        
        openai.api_key = 'API_KEY'
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]

        fav_place = getattr(request.user, 'fav_place', None)
        
        if fav_place:
            region_id = get_real_estate_id(fav_place)
            if region_id:
                top_deposits, top_savings = get_fav_place_products(region_id)
                messages.append({"role": "assistant", "content": "Here are some financial product recommendations based on your fav_place:"})
                messages.append({"role": "assistant", "content": f"Top Deposits: {top_deposits}"})
                messages.append({"role": "assistant", "content": f"Top Savings: {top_savings}"})
            else:
                messages.append({"role": "assistant", "content": "Could not find recent real estate information for your fav_place."})
        else:
            messages.append({"role": "assistant", "content": "I will explain economic concepts."})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        ai_message = response.choices[0].message['content']
        
        new_answer = Answer(answer=ai_message)
        new_answer.save()
        
        return JsonResponse({'message': ai_message})

    return render(request, 'chat.html')