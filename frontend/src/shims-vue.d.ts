/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '*.png' { 
  const src = string
  export default src
}



global { 
  interface Pagination { 
    pageSize: string
    pageNum: string
  }
}