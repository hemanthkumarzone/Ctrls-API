"""
Authentication service.
"""
import random

from datetime import (
    datetime,
    timedelta,
    timezone
)
from app.models.all_models import EmailVerification


from sqlalchemy.orm import Session

from app import models, schemas
from app.core import security
from app.core.config import settings
from app.core.security import pwd_context
from app.repositories.user_repo import user_repo
from app.schemas import user
from app.controller.email_controller import send_email

class AuthService:
    """Authentication service."""

    @staticmethod
    def authenticate_user(
        db: Session,
        username: str,
        email: str,
        password: str
    ) -> models.User | None:
        """Authenticate user."""

        user = (
            db.query(models.User)
            .filter(
                models.User.email == email,
                models.User.username == username
            )
            .first()
        )

        if not user:
            return None

        if not pwd_context.verify(
            password,
            user.password_hash
        ):
            return None

        return user

    @staticmethod
    def create_access_token(
        user: models.User
    ) -> str:
        """Create access token."""

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return security.create_access_token(
            user.id,
            expires_delta=access_token_expires,
            extra_claims={
                "tenant_id": user.tenant_id
            }
        )

    @staticmethod
    def create_refresh_token(
        user: models.User
    ) -> str:
        """Create refresh token."""

        refresh_token_expires = timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        return security.create_refresh_token(
            user.id,
            expires_delta=refresh_token_expires,
            extra_claims={
                "tenant_id": user.tenant_id
            }
        )

    @staticmethod
    def login(
        db: Session,
        username: str,
        email: str,
        password: str
    ):
        """Login user."""

        user = AuthService.authenticate_user(
            db,
            username,
            email,
            password
        )

        if (
            not user
            or not user.is_active
            or not user.is_verified
        ):
            return None

        # CHECK IF 2FA ENABLED
        if user.two_factor_enabled:

            # GENERATE OTP
            verification_code = str(
                random.randint(100000, 999999)
            )

            # SAVE OTP
            verification = EmailVerification(
    user_id=user.id,
    verification_code=verification_code,
    purpose="login_2fa",
    failed_attempts=0,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
    expires_at=datetime.now(timezone.utc)
    + timedelta(minutes=10)
)

            db.add(verification)
            db.commit()

            # SEND EMAIL
            send_email(
                to_email=user.email,
                username=user.username,
                verification_code=verification_code
            )

            return {
                "requires_2fa": True,
                "message": "2FA verification required",
                "email": user.email
            }

        # NORMAL LOGIN
        access_token = (
            AuthService.create_access_token(user)
        )

        refresh_token = (
            AuthService.create_refresh_token(user)
        )

        return schemas.Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user,
        )

    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token: str
    ) -> schemas.Token | None:
        """Refresh access token."""

        try:

            payload = security.verify_token(
                refresh_token
            )

            if payload.get("type") != "refresh":
                return None

            user_id = payload.get("sub")

        except Exception:
            return None

        user = user_repo.get(
            db,
            id=user_id
        )

        if not user or not user.is_active:
            return None

        access_token = (
            AuthService.create_access_token(user)
        )

        new_refresh_token = (
            AuthService.create_refresh_token(user)
        )

        return schemas.Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            user=user,
        )

    @staticmethod
    def create_user(
        db: Session,
        user_in: schemas.UserCreate
    ) -> models.User:
        """Create a new user."""

        existing_user = user_repo.get_by_email(
            db,
            email=user_in.email
        )

        if existing_user:
            raise ValueError(
                "User with this email already exists"
            )

        hashed_password = (
            security.get_password_hash(
                user_in.password
            )
        )

        user = models.User(
            email=user_in.email,
            username=user_in.username,
            password_hash=hashed_password,
            role=user_in.role,
            tenant_id=user_in.tenant_id,
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def register_user(
        db: Session,
        user_reg: schemas.UserRegister,
        tenant_repo
    ) -> models.User:
        """Register a new user."""

        # Generate organization slug automatically
        org_slug = (
            user_reg.company_name
            .lower()
            .replace(" ", "-")
        )

        # Check if company already exists
        tenant = tenant_repo.get_by_slug(
            db,
            org_slug
        )

        # Create company automatically
        if not tenant:

            tenant_data = schemas.TenantCreate(
    name=user_reg.company_name,
    slug=org_slug,
    metadata_={
        "admin_name": user_reg.username
    },
    is_active=True,
)

            tenant = tenant_repo.create(
                 db=db,
                 obj_in=tenant_data
            )

            # First user becomes admin
            role = "admin"

        else:

            # Existing company users
            role = "viewer"

        # Check existing email
        existing_user = (
            user_repo.get_by_email(
                db,
                email=user_reg.email
            )
        )

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        # Hash password
        hashed_password = (
            security.get_password_hash(
                user_reg.password
            )
        )

        # Create user
        user = models.User(
            email=user_reg.email,
            username=user_reg.username,
            password_hash=hashed_password,
            role=role,
            tenant_id=tenant.id,
            is_active=True,
            is_verified=False
        )

        db.add(user)
        db.commit()
        
        db.refresh(user)
        verification_code = str(
            random.randint(100000, 999999)
        )

        verification = EmailVerification(
    user_id=user.id,
    verification_code=verification_code,
    purpose="signup",
    failed_attempts=0,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
    expires_at=datetime.now(timezone.utc)
    + timedelta(minutes=10)
)

        db.add(verification)
        db.commit()
        # Send verification email
        send_email(
            to_email=user.email,
            username=user.username,
            verification_code=verification_code
        )
        return user
    
    @staticmethod
    def verify_email(
        db: Session,
        email: str,
        verification_code: str
    ):

        # Find user
        user = (
            db.query(models.User)
            .filter(
                models.User.email == email
            )
            .first()
        )

        if not user:
            raise ValueError(
                "User not found"
            )

        # Find verification code
        verification = (
            db.query(EmailVerification)
            .filter(
                EmailVerification.user_id == user.id,
                EmailVerification.verification_code == verification_code,
                EmailVerification.is_used == False
            )
            .order_by(
                EmailVerification.created_at.desc()
            )
            .first()
        )

        if not verification:
            raise ValueError(
                "Invalid verification code"
            )

        # Check expiry
        if verification.expires_at < datetime.now(timezone.utc):

            raise ValueError(
                "Verification code expired"
            )

        # Mark OTP used
        verification.is_used = True

        # Mark user verified
        user.is_verified = True

        db.commit()

        return {
            "message": "Email verified successfully"
        }
    @staticmethod
    def forgot_password(
        db: Session,
        email: str
    ):

        # FIND USER
        user = (
            db.query(models.User)
            .filter(models.User.email == email)
            .first()
        )

        if not user:
            raise ValueError("User not found")

        # GENERATE OTP
        verification_code = str(
            random.randint(100000, 999999)
        )

        # SAVE OTP
        verification = EmailVerification(
    user_id=user.id,
    verification_code=verification_code,
    purpose="forgot_password",
    failed_attempts=0,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
    expires_at=datetime.now(timezone.utc)
    + timedelta(minutes=10)
)

        db.add(verification)
        db.commit()

        # SEND EMAIL
        send_email(
            to_email=user.email,
            username=user.username,
            verification_code=verification_code
       )

        return {
            "message": "Password reset OTP sent successfully"
      }

    @staticmethod
    def reset_password(
        db: Session,
        email: str,
        verification_code: str,
        new_password: str
   ):

        # FIND USER
        user = (
            db.query(models.User)
            .filter(models.User.email == email)
            .first()
       )

        if not user:
            raise ValueError("User not found")

        # FIND OTP
        verification = (
            db.query(EmailVerification)
            .filter(
                EmailVerification.user_id == user.id,
                EmailVerification.verification_code == verification_code,
                EmailVerification.purpose == "forgot_password",
                EmailVerification.is_used == False
            )
            .order_by(
                EmailVerification.created_at.desc()
            )
            .first()
        )

        if not verification:
            raise ValueError("Invalid verification code")

        # CHECK EXPIRY
        if verification.expires_at < datetime.now(timezone.utc):

            raise ValueError(
                "Verification code expired"
            )

        # HASH NEW PASSWORD
        hashed_password =  security.get_password_hash(
                new_password
            )
        
        

        # UPDATE PASSWORD
        user.password_hash = hashed_password

        # MARK OTP USED
        verification.is_used = True
 
        db.commit()

        return {
            "message": "Password reset successful"
      }

    @staticmethod
    def resend_verification(
        db: Session,
        email: str
    ):

        # FIND USER
        user = (
            db.query(models.User)
            .filter(models.User.email == email)
            .first()
        )

        if not user:
            raise ValueError("User not found")

        # GENERATE NEW OTP
        verification_code = str(
            random.randint(100000, 999999)
        )

        # SAVE OTP
        verification = EmailVerification(
    user_id=user.id,
    verification_code=verification_code,
    purpose="signup",
    failed_attempts=0,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
    expires_at=datetime.now(timezone.utc)
    + timedelta(minutes=10)
)

        db.add(verification)
        db.commit()

        # SEND EMAIL
        send_email(
            to_email=user.email,
            username=user.username,
            verification_code=verification_code
        )

        return {
            "message": "Verification email resent successfully"
       }
    @staticmethod
    def verify_login_otp(
        db: Session,
        email: str,
        verification_code: str
    ):

        # FIND USER
        user = (
            db.query(models.User)
           .filter(models.User.email == email)
           .first()
        )

        if not user:
            raise ValueError("User not found")

        # FIND OTP
        verification = (
            db.query(EmailVerification)
            .filter(
                EmailVerification.user_id == user.id,
                EmailVerification.verification_code == verification_code,
                EmailVerification.purpose == "login_2fa",
                EmailVerification.is_used == False
            )
            .order_by(
                EmailVerification.created_at.desc()
            )
            .first()
        )

        if not verification:
            raise ValueError("Invalid verification code")

        # CHECK EXPIRY
        if verification.expires_at < datetime.now(timezone.utc):

            raise ValueError(
                "Verification code expired"
            )

        # MARK USED
        verification.is_used = True

        db.commit()

        # GENERATE TOKENS
        access_token = (
            AuthService.create_access_token(user)
        )

        refresh_token = (
            AuthService.create_refresh_token(user)
       )

        return schemas.Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user,
       )