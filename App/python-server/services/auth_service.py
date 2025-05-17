from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import random
import string
from repositories.user_repository import UserRepository
from config.secrets import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.email_tools import send_email_async

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def generate_verification_code(self):
        """Generate a random code in the format ABC-123."""
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=3))
        return f"{letters}-{digits}"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repository.get_user_by_email(email)
        if not user or not self.verify_password(password, user["password_hash"]):
            return None
        return user

    async def register_user(self, email: str, password: str):
        hashed_password = self.get_password_hash(password)
        code = self.generate_verification_code()
        try:
            # Attempt to create the user in the database
            await self.user_repository.create_user(email, hashed_password, code)
        except Exception as e:
            # If creation fails, propagate the exception (email will NOT be sent)
            raise e
        # Only send email if user creation succeeded
        await send_email_async(email, code)

    async def verify_user(self, email: str, code: str):
        """Verify the user by checking the verification code."""
        result = await self.user_repository.verify_code(email, code)
        if not result:
            raise Exception("Verification failed")
        