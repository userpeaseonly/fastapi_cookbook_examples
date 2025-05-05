from babel import Locale, negotiate_locale
from fastapi import Header, HTTPException, APIRouter, Depends
from fastapi.requests import Request
from typing import Annotated
from app.rate_limiter import limiter
from babel.numbers import get_currency_name


SUPPORTED_LOCALES = [
    "en_US",
    "fr_FR",
]

home_page_content = {
    "en_US": "Welcome to the homepage!",
    "fr_FR": "Bienvenue sur la page d'accueil!",
}

def resolve_accept_language(
    accept_language: str = Header("en-US"),
) -> Locale:
    client_locales = []
    for language_q in accept_language.split(","):
        if ";q=" in language_q:
            language, q = language_q.split(";q=")
        else:
            language, q = (language_q, float("inf"))
        try:
            Locale.parse(language, sep="-")
            client_locales.append(
                (language, float(q))
            )
        except ValueError:
            continue
    client_locales.sort(
        key=lambda x: x[1], reverse=True
    )
    locales = [locale for locale, _ in client_locales]
    locale = negotiate_locale(
        [str(locale) for locale in locales],
        SUPPORTED_LOCALES,
    )
    if locale is None:
        locale = "en_US"
    return locale


async def get_currency(language: Annotated[resolve_accept_language, Depends()]) -> str:
    currencies = {
        "en_US": "USD",
        "fr_FR": "EUR",
    }
    return currencies.get(language, "USD")

router = APIRouter(tags=["Localized Content Endpoints"])

@router.get("/homepage")
@limiter.limit("2/minute")
async def home(
    request: Request,
    language: Annotated[resolve_accept_language, Depends()],
):

    return {"message": home_page_content[language]}

@router.get("/show/currency")
async def show_currency(
    currency: Annotated[get_currency, Depends()],
    language: Annotated[
        resolve_accept_language,
        Depends(use_cache=True)
    ],
):
    currency_name = get_currency_name(
        currency, locale=language
    )
    return {
        "currency": currency,
        "currency_name": currency_name,
    }