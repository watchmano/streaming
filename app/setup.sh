#!/bin/bash

# 프로젝트 루트에서 실행할 것

echo "📦 가상환경 생성 중..."
python3 -m venv venv

echo "✅ 가상환경 생성 완료: ./venv"

echo "🐍 가상환경 활성화"
source venv/bin/activate

echo "📄 requirements.txt 기반으로 패키지 설치 중..."
pip3 install --upgrade pip
pip3 install -r ./requirements.txt

echo "✅ 설치 완료! 이제 다음 명령으로 서버 실행 가능:"
echo "source venv/bin/activate && uvicorn app.main:app --reload"
