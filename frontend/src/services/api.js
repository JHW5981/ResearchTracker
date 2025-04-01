import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000'
})

export const searchPapers = async (params) => {
  try {
    const response = await api.post('/api/papers', params)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.error || '请求失败')
  }
}