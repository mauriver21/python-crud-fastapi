from interfaces.DbConfig import DbConfig


class Config:
    environment: str
    allowedOrigins: str
    port: int
    jwtExpiresIn: str
    jwtSecretKey: str
    diskStoragePath: str
    db: DbConfig
