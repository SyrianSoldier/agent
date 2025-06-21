import axios, {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig
} from 'axios'

// 定义后端接口返回数据的结构
interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  success: boolean
}

export interface Pagination { 
  pagesize: string | number
  pagenum: string | number
}

export interface ListResponse<T = any> { 
  total: string | number
  list: T[]
}


// 创建 axios 实例
const http: AxiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL, // 基础URL
  timeout: 10000,                             // 请求超时时间
  headers: {
    'Content-Type': 'application/json;charset=UTF-8'
  }
})

// 请求拦截器
http.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 在发送请求之前做些什么
    // 例如：如果需要token，可以在这里统一设置
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error: any) => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 响应拦截器
http.interceptors.response.use(
  (response: AxiosResponse) => {
    // 对响应数据做点什么
    // 例如：统一处理返回的数据结构
    if (response.data.code === 200 || response.data.success === true) {
      return response.data // 直接返回data字段
    } else {
      // 可以在这里处理业务错误
      console.error(response.data.message || 'Error')
      return Promise.reject(response.data)
    }
  },
  (error: any) => {
    // 对响应错误做点什么
    // 例如：统一处理HTTP错误状态码
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 处理未授权
          break;
        case 403:
          // 处理禁止访问
          break;
        case 404:
          // 处理资源不存在
          break;
        case 500:
          // 处理服务器错误
          break;
        default:
        // 处理其他错误
      }
    }
    return Promise.reject(error);
  }
)

const request = async <R = any>(params: AxiosRequestConfig): Promise<ApiResponse<R>> => {
  return (await http.request(params)) as ApiResponse<R>
}

export default request
