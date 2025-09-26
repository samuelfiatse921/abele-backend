from typing import Sequence

from sqlalchemy import Row

from app.schema.deployment import GetDeployment
from app.schema.following import GetFollowing
from app.schema.grapejs_project import GetProject
from app.schema.asset_upload import GetAsset
from app.schema.uploaded_template import GetJoinedUploadedUserTemplate, TemplateFiles, GetUploadedTemplate
from app.schema.user import GetUser, GetName, GetLocation, GetStreet, GetCoordinates, GetDate, GetRegistered, GetID, \
    GetPicture, GetUserCredentials
from app.schema.user_template import GetUserTemplate
from app.schema.wallet import GetWallet
from app.user.models import Payment
from app.schema.payment import GetPayment
from app.user.models.deployment import Deployment
from app.user.models.following import Following
from app.user.models.grapejs_project import GrapeJSProject
from app.user.models.asset_upload import UploadedAsset
from app.user.models.uploaded_template import UploadedTemplate
from app.user.models.user import User
from app.user.models.user_template import UserTemplate
from app.user.models.wallet import Wallet
from app.utils.utils import get_age


def map_to_following(
    record: Following
) -> GetFollowing:
    return GetFollowing(
        id=record.id,
        userId=record.user_id,
        followingUserId=record.following_user_id,
        createdOn=record.created_on,
        updatedOn=record.updated_on
    )


def map_to_following_list(
    records: Sequence[Following],
) -> list[GetFollowing]:
    result = []
    for record in records:
        record = map_to_following(record)
        result.append(record)
    return result


def map_to_payment(
    record: Payment
) -> GetPayment:
    return GetPayment(
        id=record.id,
        currency=record.currency,
        amount=record.amount,
        reference=record.reference,
        external_reference=record.external_reference,
        userId=record.user_id,
        processorId=record.payment_nonce,
        narration=record.narration,
        status=record.status,
        createdOn=record.created_on,
        updatedOn=record.updated_on
    )


def map_to_payment_list(
    records: Sequence[Payment],
) -> list[GetPayment]:
    result = []
    for record in records:
        record = map_to_payment(record)
        result.append(record)
    return result


def map_to_uploaded_template(
    record: UploadedTemplate
) -> GetUploadedTemplate:
    return GetUploadedTemplate(
        id=record.id,
        image=record.image,
        ownerId=record.owner_id,
        templateName=record.name,
        price=record.price,
        coin=record.coin,
        tier=record.tier,
        category=record.category,
        under=record.under,
        liveDemo=record.live_demo,
        templateFiles=TemplateFiles(
            htmlFiles=record.html_files,
            cssFiles=record.css_files,
            jsFiles=record.js_files
        ),
        reviews=record.reviews,
        rating=record.rating,
        createdOn=record.created_on,
        updatedOn=record.updated_on
    )


def map_to_joined_uploaded_template_and_user(
    template_record: UploadedTemplate,
    user_record: User
) -> GetJoinedUploadedUserTemplate:
    return GetJoinedUploadedUserTemplate(
        id=template_record.id,
        image=user_record.picture_medium,
        owner=f"{user_record.first_name} {user_record.last_name}",
        template=template_record.image,
        templateName=template_record.name,
        price=template_record.price,
        coin=template_record.coin,
        tier=template_record.tier,
        category=template_record.category,
        liveDemo=template_record.live_demo,
        under=template_record.under,
        templateFiles=TemplateFiles(
            htmlFiles=template_record.html_files,
            cssFiles=template_record.css_files,
            jsFiles=template_record.js_files
        ),
        reviews=template_record.reviews,
        rating=template_record.rating,
        createdOn=template_record.created_on,
        updatedOn=template_record.updated_on
    )


def map_to_joined_uploaded_template_and_user_list(
    records: Sequence[Row[tuple[UploadedTemplate, User]]],
) -> list[GetJoinedUploadedUserTemplate]:
    result = []
    for record in records:
        uploaded_template, user = record
        records = map_to_joined_uploaded_template_and_user(uploaded_template, user)
        result.append(records)
    return result


def map_to_joined_uploaded_user_template_list(
    records: Sequence[Row[tuple[UploadedTemplate, User, UserTemplate]]],
) -> list[GetJoinedUploadedUserTemplate]:
    result = []
    for record in records:
        uploaded_template, user, _ = record
        records = map_to_joined_uploaded_template_and_user(uploaded_template, user)
        result.append(records)
    return result


def map_to_user(
    record: User
) -> GetUser:
    name = GetName(
        first=record.first_name,
        last=record.last_name,
        title=record.title,
        username=record.username
    )
    street = GetStreet(
        number=record.street_number,
        name=record.street_name
    )
    coordinates = GetCoordinates(
        longitude=record.longitude,
        latitude=record.latitude
    )
    location = GetLocation(
        street=street,
        city=record.city,
        state=record.state,
        country=record.country,
        postcode=record.postcode,
        coordinates=coordinates
    )
    dob = GetDate(
        date=record.dob,
        age=str(get_age(record.dob))
    )
    registered = GetRegistered(
        date=record.created_on,
        age=str(get_age(record.dob))
    )
    picture = GetPicture(
        large=record.picture_large,
        medium=record.picture_medium,
        thumbnail=record.picture_thumbnail
    )

    return GetUser(
        gender=record.gender,
        name=name,
        location=location,
        email=record.email,
        dob=dob,
        registered=registered,
        phone=record.phone,
        cell=record.cell,
        id=GetID(value=str(record.id)),
        picture=picture,
        nat=record.nat,
    )


def map_to_user_list(
    records: Sequence[UploadedTemplate],
) -> list[GetUser]:
    result = []
    for record in records:
        records = map_to_user(record)
        result.append(records)
    return result


def map_to_wallet(
    record: Wallet
) -> GetWallet:
    return GetWallet(
        id=record.id,
        userId=record.user_id,
        balance=record.balance,
        createdOn=record.created_on,
        updatedOn=record.updated_on
    )


def map_to_wallet_list(
    records: Sequence[Wallet],
) -> list[GetWallet]:
    result = []
    for record in records:
        records = map_to_wallet(record)
        result.append(records)
    return result


def map_to_user_template(
    record: UserTemplate
) -> GetUserTemplate:
    return GetUserTemplate(
        id=record.id,
        templateId=record.template_id,
        userId=record.user_id,
        createdOn=record.created_on,
        updatedOn=record.updated_on
    )


def map_to_user_credentials(
    record: User
) -> GetUserCredentials:
    return GetUserCredentials(
        userId=record.id,
        username=record.username,
        email=record.email,
        hashed_password=record.hashed_password
    )


def map_to_deployment(
    record: Deployment
) -> GetDeployment:
    return GetDeployment(
        id=record.id,
        name=record.name,
        deploymentSupportCost=record.deployment_support_cost,
        deploymentSupportDescription=record.deployment_support_description,
        domainSupportCost=record.domain_support_cost,
        domainSupportDescription=record.domain_support_description,
        createdOn=record.created_on,
        updatedOn=record.updated_on
    )


def map_to_deployment_list(
    records: Sequence[Deployment],
) -> list[GetDeployment]:
    result = []
    for record in records:
        records = map_to_deployment(record)
        result.append(records)
    return result


def map_to_grape_js_project(
    record: GrapeJSProject
) -> GetProject:
    return GetProject(
        id=record.id,
        userId=record.user_id,
        templateId=record.template_id,
        data=record.data,
        createdOn=record.created_on,
        updatedOn=record.updated_on
    )


def map_to_uploaded_asset(
    record: UploadedAsset
) -> GetAsset:
    return GetAsset(
        id=record.id,
        fileName=record.file_name,
        filePath=record.file_path,
        createdOn=record.created_on
    )


def map_to_uploaded_asset_list(
    records: Sequence[UploadedAsset],
) -> list[GetAsset]:
    result = []
    for record in records:
        records = map_to_uploaded_asset(record)
        result.append(records)
    return result


