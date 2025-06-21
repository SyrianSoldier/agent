export type ChatRole = 'USER' | 'ASSISTANT'

export interface ChatSession { 
  uuid: string
  title?: string
}


export interface ChatMessage {
  role: ChatRole
  content: string
  thinking_content?: string
  gmt_modified: string
  [key: string]: any
}