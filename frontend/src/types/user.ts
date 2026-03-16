export interface UserInfo {
  id: number
  username: string
  email: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}
