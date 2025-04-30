import axios from 'axios'
import { useRouter } from 'vue-router'

export function useAuth() {
  const router = useRouter()

  const handleAuthError = async (error, retryFunction) => {
    if (error.response && error.response.status === 401) {
      try {
        const refresh = localStorage.getItem('refresh_token')
        const refreshResponse = await axios.post('http://127.0.0.1:8000/api/token/refresh/', { refresh })
        const newAccess = refreshResponse.data.access
        localStorage.setItem('access_token', newAccess)
        if (retryFunction) await retryFunction()
      } catch (refreshError) {
        console.error('Refresh token expired, redirecting to login')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
      }
    } else {
      console.error('Other error:', error)
    }
  }

  return { handleAuthError }
}
