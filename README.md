# 코딩 테스트 플랫폼 API

## 프로젝트 소개

<p align="justify">
캐싱, 메시지 큐, 테스트 코드 작성, Swagger에 대한 학습을 진행하기 위해 진행한 사이드 프로젝트입니다.<br>
대용량 트래픽을 고려한 구조를 채용하여, 캐싱과 메시지 큐를 이용하여 성능을 보장하도록 구현했습니다.<br>
구현한 로직에 대한 테스트를 작성하고, Swagger를 이용하여 API 문서화를 진행할 예정입니다.<br>
이 모든 과정은 직접 설계하고 구현했습니다.
</p><br>

## 기술 스택

| Python | Django |  Django REST framework   |
| :----: | :----: | :----------------------: |
|  3.10  |   4.1  |          3.14            |
<br>

## ERD
<img src="https://user-images.githubusercontent.com/82267811/225641550-2ce15d64-e918-48c6-a61b-20fd954e708a.png">
<br>

## API 예시

* Swagger를 통한 API 문서화 예정

![image](https://user-images.githubusercontent.com/82267811/225653214-a8db59db-5f09-4975-a6fb-c11e50f060c2.png)
![image](https://user-images.githubusercontent.com/82267811/225652451-cdbb24cf-e290-428f-909a-c0870c281083.png)
![image](https://user-images.githubusercontent.com/82267811/225652697-09f87ad2-5ec5-4d9a-af26-3384636160f7.png)
![image](https://user-images.githubusercontent.com/82267811/225653400-a68cd628-c633-4955-b03a-85d27100c5f3.png)

<br>

## 배운 점 & 아쉬운 점
#### 중간 평가: 시작(3월3일) ~ 2주차(3월 16일)
<p align="justify">
약 2주 간의 기간이었지만 직장 생활과 병행하면서 투자하는 시간이 적었던 것이 아쉽다.<br>
대용량 트래픽을 처리하는 구조에서 중요한 역할을 하는 캐싱과 메시지 큐에 대한 이해를 갖고, 사용해본 경험이 생겼다는 점이 좋았다.<br>
그러나 테스트 코드와 Swagger 적용에 대해서는 아쉬운 점이 있다.<br><br>
먼저 테스트 코드 작성에 관련된 부분은 모델 생성과 관련된 간단한 정도의 테스트만을 작성하였다는 것이 아쉽다.<br>
모델 생성에 대한 테스트만으로는 전체 로직이 제대로 동작하는지를 확인하기 어렵다.<br>
따라서 로직의 각 단계별로 테스트 코드를 작성 예정이다.

Swagger를 이용한 API 문서화는 drf-spectacular (https://drf-spectacular.readthedocs.io/en/latest/) 를 적용만 하고, 진행하지 못하였다.<br>
추후 drf-spectacular에 대한 학습 과정을 거쳐 진행할 예정이다.
</p>
