#!/bin/bash

# 현재 위치에서 app 디렉토리가 있는지 확인
if [ ! -d "./app" ]; then
  echo "❌ Error: 'app/' 디렉토리를 찾을 수 없습니다. 프로젝트 루트에서 실행하세요."
  exit 1
fi

# 실행
echo "🚀 FastAPI 서버 실행 중 (http://localhost:8000/static/index.html)"
PYTHONPATH=./app uvicorn app.main:app --reload --reload-exclude output/*
