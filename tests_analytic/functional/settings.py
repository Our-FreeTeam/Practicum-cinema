from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    keycloak_url: str = Field(..., env='KEYCLOAK_URL')
    auth_url: str = Field(..., env='AUTH_URL')
    client_id: str = Field(..., env='KEYCLOAK_CLIENT_ID')
    realm_name: str = Field(..., env='KEYCLOAK_REALM_ID')
    client_secret_key: str = Field(..., env='KEYCLOAK_SECRET_KEY')
    service_account: str = Field(..., env='KEYCLOAK_SERVICE_ACCOUNT')
    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    helios_api_token: str = Field(..., env='HELIOS_API_TOKEN')
    helios_enabled: bool = Field(..., env='HELIOS_ENABLED')

    analytic_url: str = Field(..., env='ANALYTIC_URL')
    ugc_api_service: str = Field(..., env='UGC_API_URL')

class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
