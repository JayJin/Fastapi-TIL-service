# FastAPI Clean Architecture 프로젝트

FastAPI와 클린 아키텍처 원칙을 따르는 사용자 관리 시스템입니다. 계층별 분리를 통해 유지보수성과 확장성을 높였습니다.

## 📋 목차
- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [API 엔드포인트](#api-엔드포인트)
- [아키텍처 설명](#아키텍처-설명)

---

## 프로젝트 개요

본 프로젝트는 FastAPI를 사용하여 구현된 사용자 관리 시스템으로, 다음의 기능을 포함합니다:

- **사용자 관리**: 회원가입, 로그인, 프로필 조회 및 수정
- **인증/인가**: JWT 토큰 기반 인증, 역할 기반 접근 제어(RBAC)
- **데이터 암호화**: 비밀번호 해싱 및 암호화
- **데이터베이스 마이그레이션**: Alembic을 통한 스키마 관리

---

## 기술 스택

| 분류 | 기술 |
|------|------|
| **Framework** | FastAPI 0.127.0+ |
| **Database** | MySQL / SQLAlchemy 2.0+ |
| **ORM** | SQLAlchemy |
| **마이그레이션** | Alembic 1.17.2+ |
| **의존성 주입** | dependency-injector 4.48.3+ |
| **인증** | python-jose, JWT |
| **암호화** | bcrypt, passlib |
| **유틸** | Pydantic, Python-ULID, python-dotenv |

---

## 프로젝트 구조

```
fastapi_test/
├── main.py                          # FastAPI 앱 초기화 및 라우터 등록
├── config.py                        # 환경 설정 (Settings)
├── containers.py                    # 의존성 주입 컨테이너 정의
├── database.py                      # 데이터베이스 연결 설정
├── pyproject.toml                   # 프로젝트 의존성 정의
├── .env                             # 환경 변수 파일
│
├── user/                            # 사용자 도메인 모듈
│   ├── application/                 # 애플리케이션 계층 (비즈니스 로직)
│   │   └── user_service.py          # 사용자 관련 서비스 클래스
│   │
│   ├── domain/                      # 도메인 계층 (엔티티 & 인터페이스)
│   │   ├── user.py                  # User 도메인 엔티티
│   │   └── repository/
│   │       └── user_repo.py         # IUserRepository 추상 인터페이스
│   │
│   ├── infra/                       # 인프라 계층 (DB 연동)
│   │   ├── db_models/
│   │   │   └── user.py              # SQLAlchemy ORM 모델
│   │   └── repository/
│   │       └── user_repo.py         # UserRepository 실제 구현
│   │
│   └── interface/                   # 인터페이스 계층 (HTTP 컨트롤러)
│       └── controllers/
│           └── user_crotroller.py   # FastAPI 라우터 & 엔드포인트
│
├── common/                          # 공통 유틸리티
│   ├── auth.py                      # JWT 인증, 역할 정의
│   ├── logger.py                    # 로깅 설정
│   └── messaging.py                 # 메시지 전송 유틸
│
├── utils/                           # 프로젝트 유틸리티
│   ├── crypto.py                    # 암호화 관련 유틸
│   └── db_utils.py                  # DB 관련 헬퍼 함수
│
└── migrations/                      # Alembic DB 마이그레이션
    ├── env.py                       # Alembic 설정
    ├── script.py.mako               # 마이그레이션 스크립트 템플릿
    └── versions/                    # 마이그레이션 히스토리
        └── 2025_12_26_2149-*.py     # 마이그레이션 파일
```

---

## 설치 및 실행

### 1. 환경 구성

```bash
# 프로젝트 클론
git clone <repository>
cd fastapi_test

# Python 3.12 이상 필요
python --version
```

### 2. 가상 환경 설정 및 의존성 설치

```bash
# uv를 사용하는 경우
uv sync

# pip를 사용하는 경우
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일 생성 (프로젝트 루트):

```env
DATABASE_USERNAME=root
DATABASE_PASSWORD=your_password
JWT_SECRET=your_secret_key_here
```

### 4. 데이터베이스 초기화

```bash
# Alembic 마이그레이션 실행
alembic upgrade head
```

### 5. 서버 실행

```bash
# 개발 서버 실행 (자동 리로드)
python main.py

# 또는
uvicorn main:app --reload
```

서버는 `http://127.0.0.1:8000`에서 실행됩니다.
- API 문서: `http://127.0.0.1:8000/docs` (Swagger UI)
- 대체 문서: `http://127.0.0.1:8000/redoc` (ReDoc)

---

## API 엔드포인트

### 사용자 관리

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|-----------|------|---------|
| `POST` | `/users` | 사용자 생성(회원가입) | ❌ |
| `POST` | `/users/login` | 로그인 (JWT 토큰 발급) | ❌ |
| `GET` | `/users/me` | 현재 사용자 정보 조회 | ✅ |
| `GET` | `/users/{user_id}` | 특정 사용자 조회 | ✅ |
| `PUT` | `/users/{user_id}` | 사용자 정보 수정 | ✅ |
| `DELETE` | `/users/{user_id}` | 사용자 삭제 | ✅ (ADMIN) |

### 요청/응답 예시

#### 회원가입
```bash
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

**응답 (201 Created):**
```json
{
  "id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-12-29T10:30:00",
  "updated_at": "2025-12-29T10:30:00"
}
```

#### 로그인
```bash
POST /users/login
Content-Type: application/x-www-form-urlencoded

username=john@example.com&password=SecurePassword123
```

**응답 (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 현재 사용자 조회
```bash
GET /users/me
Authorization: Bearer <token>
```

#### 사용자 정보 수정
```bash
PUT /users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Doe",
  "password": "NewPassword456"
}
```

---

## 아키텍처 설명

### 클린 아키텍처 4계층

#### 1. **Interface (인터페이스 계층)**
- **파일**: `user/interface/controllers/user_crotroller.py`
- **역할**: HTTP 요청/응답 처리
- **담당**: FastAPI 라우터, 요청 검증, 응답 형식화
- **의존성**: application 계층에 의존

```python
@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.create_user(...)
```

#### 2. **Application (애플리케이션 계층)**
- **파일**: `user/application/user_service.py`
- **역할**: 비즈니스 로직 처리
- **담당**: 사용자 생성, 수정, 조회 등 핵심 로직
- **의존성**: domain 계층에 의존

```python
class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def create_user(self, name: str, email: str, password: str):
        # 비즈니스 로직
        user = User(...)
        self.user_repo.save(user)
        return user
```

#### 3. **Domain (도메인 계층)**
- **파일**: `user/domain/`
- **역할**: 핵심 엔티티 및 도메인 규칙 정의
- **담당**: `User` 엔티티, `IUserRepository` 추상 인터페이스
- **특징**: 외부 의존성 없음 (프레임워크 독립)

```python
@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError
```

#### 4. **Infrastructure (인프라 계층)**
- **파일**: `user/infra/`
- **역할**: 실제 데이터베이스 연동
- **담당**: ORM 모델, 저장소 구현체
- **의존성**: domain 계층의 추상화 인터페이스 구현

```python
class UserRepository(IUserRepository):
    def save(self, user: User):
        db_user = User(...)  # ORM 모델
        db.add(db_user)
        db.commit()
    
    def find_by_email(self, email: str) -> User:
        # DB 조회 후 도메인 객체로 변환
```

### 요청 흐름 (POST /users)

```
1. HTTP Request → Interface (Controller)
   ├─ 요청 데이터 검증 (Pydantic)
   ├─ 의존성 주입 (DI Container)
   └─ service.create_user() 호출
   
2. Application (Service)
   ├─ 비즈니스 로직 처리
   ├─ User 도메인 객체 생성
   └─ repository.save() 호출
   
3. Domain (Repository Interface)
   └─ 추상 인터페이스 정의
   
4. Infrastructure (Repository Implementation)
   ├─ 도메인 객체 → ORM 모델 변환
   ├─ DB에 저장
   └─ 결과 반환
   
5. HTTP Response
   └─ 생성된 사용자 정보 반환
```

### 의존성 주입 (Dependency Injection)

`containers.py`에서 DI 컨테이너 정의:

```python
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user"],
    )
    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)
```

`main.py`에서 wiring 활성화:

```python
app.container = Container()
app.container.wire(packages=["user.interface.controllers"])
```

컨트롤러에서 사용:

```python
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    ...
```

---

## 주요 기능 설명

### 1. 사용자 인증 (JWT)

- **토큰 생성**: `common/auth.py`의 `create_access_token()`
- **토큰 검증**: `get_current_user()` 의존성
- **역할 기반 접근**: `Role` Enum (ADMIN, USER)

```python
token = create_access_token(
    data={"sub": user.id, "role": user.role},
    expires_delta=timedelta(hours=1)
)
```

### 2. 비밀번호 암호화

- **해싱**: `utils/crypto.py`의 `Crypto` 클래스
- **알고리즘**: bcrypt
- **사용**: 가입 및 수정 시 비밀번호 암호화

```python
encrypted_password = self.crypto.encrypt(plain_password)
```

### 3. 데이터베이스 마이그레이션

Alembic을 통한 스키마 버전 관리:

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "add user table"

# 마이그레이션 적용
alembic upgrade head

# 이전 버전으로 롤백
alembic downgrade -1
```

### 4. 환경 설정

`config.py`에서 Pydantic BaseSettings 사용:

```python
class Settings(BaseSettings):
    database_username: str
    database_password: str
    jwt_secret: str
```

---

## 에러 처리

### 예외 핸들러

`main.py`에서 검증 에러를 422에서 400으로 변환:

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=str(exc.errors()))
```

### 주요 에러 응답

- `400 Bad Request`: 요청 데이터 검증 실패
- `401 Unauthorized`: 인증 필요 또는 토큰 만료
- `403 Forbidden`: 권한 부족
- `422 Unprocessable Entity`: 중복 이메일 등 비즈니스 규칙 위반
- `500 Internal Server Error`: 서버 오류

---

## 개발 팁

### 1. 새로운 도메인 추가

1. `{domain}/domain/` - 엔티티 및 저장소 인터페이스 정의
2. `{domain}/application/` - 서비스 로직 구현
3. `{domain}/infra/` - ORM 모델 및 저장소 구현
4. `{domain}/interface/controllers/` - 라우터 및 엔드포인트
5. `containers.py`에 DI 등록
6. `main.py`에 라우터 include

### 2. DB 마이그레이션

```bash
# 변경사항 감지하여 마이그레이션 생성
alembic revision --autogenerate -m "describe your change"

# 마이그레이션 파일 검토 후 적용
alembic upgrade head
```

### 3. 테스트

```bash
# 테스트 실행
python -m pytest

# 테스트 커버리지
python -m pytest --cov
```

---

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/)
- [dependency-injector 공식 문서](https://python-dependency-injector.ets-labs.org/)
- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [클린 아키텍처 (Clean Architecture)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## 라이센스

MIT License - 자유롭게 사용 가능

## 문의

프로젝트에 대한 질문이나 제안은 이슈를 통해 문의해주세요.
