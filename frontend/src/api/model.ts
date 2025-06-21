import requst, { Pagination, ListResponse } from "./request"

namespace ModelAPI {
  export type ModelStatus = "Unconfigured" | "Configured"

  export interface model_list { 
    response: ListResponse<{
      model_name: string,
      status: ModelStatus
    }>
  }

}

export const create_model = (model_name:string) => { 
  return requst({
    method: "post",
    url: "/model/create",
    params: {},
    data: {model_name}
  }) 
}


export const delete_model = (id:string) => { 
  return requst({
    method: "post",
    url: "/model/delete",
    params: {},
    data: {id}
  }) 
}


export const model_list = () => { 
  return requst<ModelAPI.model_list["response"]>({
    method: "get",
    url: "/model/list",
    params: {},
    data: {}
  }) 
}

export const avaliable_model_list = () => { 
  return requst({
    method: "get",
    url: "/model/avaliable_model/list",
    params: {},
    data: {}
  }) 
}




