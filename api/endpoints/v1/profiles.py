from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.profile.reg_email import send_reg_email
from config.database import get_session

from api.models.profile import Profile
from api.schemas.profiles import GetProfile, EmailStr, CreateProfile, Test, UpdateProfile
from api.services.files.files import is_file_valid, upload_file_to_s3
from api.services.profile.location import convert_coords_to_locs
from api.services.profile.profile import get_low_password_hash

api_profiles = APIRouter()


@api_profiles.post("/simple-create/profile/", response_model=GetProfile)
async def simple_create(
        profile: CreateProfile,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_session)
):
    query = await db.execute(
        select(Profile).where(Profile.email == profile.email)
    )
    if query.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="The profile with this email is already exits")

    hashed_password = get_low_password_hash(profile.password)
    profile.password = hashed_password

    new_profile = Profile(**profile.dict(exclude_none=True))
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    # send_reg_email(profile.email)
    background_tasks.add_task(send_reg_email, profile.email)

    return new_profile


@api_profiles.get("/profiles/", response_model=list[GetProfile])
async def get_list(db: AsyncSession = Depends(get_session)):
    profiles = await db.execute(
        select(Profile)
    )
    return profiles.scalars().all()


@api_profiles.get("/profiles/pagination/", response_model=list[GetProfile])
async def get_list(page: int, page_size: int, db: AsyncSession = Depends(get_session)):
    offset = (page - 1) * page_size
    profiles = await db.execute(
        select(Profile).offset(offset).limit(page_size)
    )
    return profiles.scalars().all()


@api_profiles.get("/profile/{profiles_id}/", response_model=GetProfile)
async def retrieve(profiles_id: int, db: AsyncSession = Depends(get_session)):
    profiles = await db.execute(
        select(Profile).where(Profile.id == profiles_id)
    )
    profile = profiles.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=400, detail="The profile with this id is already exits")
    return profile


@api_profiles.patch("profile/update/{profiles_id}", response_model=GetProfile)
async def profile_update(
        profiles_id: int,
        profile: UpdateProfile,
        db: AsyncSession = Depends(get_session)
):
    profile_q = await db.execute(
        select(Profile).where(Profile.id == profiles_id)
    )
    if profile_q.scalar_one_or_none() is None:
        raise HTTPException(status_code=400, detail="The profile with this id does not exist")

    await db.execute(
        update(Profile).where(Profile.id == profiles_id).values(**profile.dict(exclude_none=True))
    )
    await db.commit()

    res = await db.execute(select(Profile).where(Profile.id == profiles_id))

    return res.scalar_one_or_none()


@api_profiles.delete("/profile/delete/{profile_id}", status_code=204)
async def profile_delete(
        profile_id: int,
        db: AsyncSession = Depends(get_session)
):
    await db.execute(
        delete(Profile).where(Profile.id == profile_id)
    )
    await db.commit()
    return {"message": f"User with id {profile_id} deleted successfully"}


# regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
@api_profiles.post("/profile/", response_model=GetProfile)
async def create(
        background_tasks: BackgroundTasks,
        avatar: UploadFile = File(default=None, description="size < 20 MB, allowed_extensions = jpg, jpeg, png"),
        email: EmailStr = Form(..., example='user@example.com'),
        password: str = Form(..., min_length=8),
        first_name: str = Form(..., max_length=55, min_length=2),
        last_name: str = Form(default=None),
        lat: float = Form(default=None),
        lng: float = Form(default=None),
        db: AsyncSession = Depends(get_session)
):
    query = await db.execute(
        select(Profile).where(Profile.email == email)
    )
    if query.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="The profile with this email is already exits")

    hashed_password = get_low_password_hash(password)

    if avatar:
        is_avatar_valid = await is_file_valid(avatar)
        if not is_avatar_valid:
            raise HTTPException(status_code=400, detail="Profile not found")
        image_path = 'profile/avatars/' + f'user_{email}/' + avatar.filename
        avatar_path = await upload_file_to_s3(avatar, image_path)
    else:
        avatar_path = None

    if lat and lng:
        country, city = await convert_coords_to_locs(lat, lng)
    else:
        country, city = None, None

    is_profile_valid = CreateProfile(
        avatar=avatar_path, email=email, password=hashed_password, first_name=first_name,
        last_name=last_name, lat=lat, lng=lng, country=country, city=city
    )

    new_profile = Profile(**is_profile_valid.dict(exclude_none=True))
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    # send_reg_email(profile.email)
    background_tasks.add_task(send_reg_email, email)

    return new_profile

















### TEST


@api_profiles.post("/test/profile/")
async def simple_create(
        test: Test = Form(...),
        file: UploadFile = File(...),
):
    """ Parse schema test """
    return {"file": file.filename, "test": test}
