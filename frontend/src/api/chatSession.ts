import requst, { Pagination, ListResponse } from "./request"

namespace ChatAPI {
  export interface ChatSession {
      gmt_create: string
      gmt_modified: string
      title: string
      uuid: string
      [property: string]: any
    }
  
  export interface create_chat_session { 
    response: ChatSession
  }

  export interface chat_session_detail { 
    response: ChatSession
  }

   export interface chat_session_list { 
    response: ListResponse<ChatSession>
  }
}

export const create_chat_session = (title:string) => { 
  return requst<ChatAPI.create_chat_session["response"]>({
    method: "post",
    url: "/chat_session/create",
    params: {},
    data: {title}
  }) 
}


export const delete_chat_session = (uuid:string) => { 
  return requst({
    method: "post",
    url: "/chat_session/delete",
    params: {},
    data: {uuid}
  }) 
}


export const chat_session_detail = (uuid:string) => { 
  return requst<ChatAPI.chat_session_detail["response"]>({
    method: "get",
    url: "/chat_session/detail",
    params: {},
    data: {uuid}
  }) 
}

export const chat_session_list = (params: Pagination) => { 
  return requst<ChatAPI.chat_session_list["response"]>({
    method: "get",
    url: "/chat_session/rename",
    params: {...params},
    data: {...params}
  }) 
}

export const chat_session_rename = (title:string, uuid:string) => { 
  return requst({
    method: "post",
    url: "/chat_session/rename",
    params: {},
    data: {uuid, title}
  }) 
}




