from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    keycloak_url: str = Field(..., env='KEYCLOAK_URL')
    client_id: str = Field(..., env='KEYCLOAK_CLIENT_ID')
    realm_name: str = Field(..., env='KEYCLOAK_REALM_ID')
    client_secret_key: str = Field(..., env='KEYCLOAK_SECRET_KEY')
    service_account: str = Field(..., env='KEYCLOAK_SERVICE_ACCOUNT')

    keycloak_admin_login: str = Field(..., env='KEYCLOAK_ADMIN')
    keycloak_admin_password: str = Field(..., env='KEYCLOAK_ADMIN_PASSWORD')
    keycloak_service_email: str = Field(..., env='KEYCLOAK_SERVICE_EMAIL')
    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    keycloak_realm_su: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU')
    keycloak_realm_su_psw: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU_PSW')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    rate_limit: int = Field(..., env='SHIELD_RATE_LIMIT')
    time_period: int = Field(..., env='SHIELD_TIME_PERIOD')

    helios_api_token: str = Field(..., env='HELIOS_API_TOKEN')
    helios_enabled: bool = Field(..., env='HELIOS_ENABLED')

    recapcha_api_key: str = Field(..., env='RECAPCHA_API_KEY')
    recapcha_enabled: bool = Field(..., env='RECAPCHA_ENABLED')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
