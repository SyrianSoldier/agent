import React, { useLayoutEffect, useRef, useState } from 'react';
import { Input, Button, List, Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { PageContainer } from '@ant-design/pro-components';

const { TextArea } = Input;

enum ChatRoleEnum {
  user= "user",
  bot= "bot"
}

interface Message {
  content: string;
  role: ChatRoleEnum;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const socketRef = useRef<WebSocket>();

  // 初始化 WebSocket 连接
  const initWebsocket = () => {
    socketRef.current = new WebSocket('ws://localhost:1080/api/chat');

    // 监听连接成功事件
    socketRef.current.onopen = () => {
      console.log('WebSocket connection opened');
    };

    // 监听消息事件
    socketRef.current.onmessage = (event) => {
      const botMessage: Message = {content: JSON.parse(event.data), role: ChatRoleEnum.bot}
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    };

    // 监听连接关闭事件
    socketRef.current.onclose = () => {
      console.log('WebSocket connection closed');
    };

    // 监听错误事件
    socketRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  };

  // 关闭 WebSocket 连接
  const closeWebsocket = () => {
    if (socketRef.current) {
      socketRef.current.close();
    }
  };

  // 发送消息
  const handleSend = () => {
    if (inputValue.trim() && socketRef.current) {
      // 添加用户消息
      const userMessage: Message = { content: inputValue, role: ChatRoleEnum.user };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInputValue('');

      // 通过 WebSocket 发送消息
      socketRef.current.send(inputValue);
    }
  };

  // 组件挂载时初始化 WebSocket
  useLayoutEffect(() => {
    initWebsocket();

    // 组件卸载时关闭 WebSocket
    return () => {
      closeWebsocket();
    };
  }, []);

  return (
    <PageContainer title="Chat Interface" header={{ title: 'DeepSeek Chat', extra: [] }}>
      <div style={{ display: 'flex', flexDirection: 'column', height: '90vh', padding: '24px' }}>
        {/* 消息列表 */}
        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '16px' }}>
          <List
            dataSource={messages}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    <Avatar
                      icon={<UserOutlined />}
                      style={{ backgroundColor: item.role === ChatRoleEnum.user ? '#87d068' : '#f56a00' }}
                    />
                  }
                  title={item.role === ChatRoleEnum.user ? 'You' : 'Bot'}
                  description={item.content}
                />
              </List.Item>
            )}
          />
        </div>

        {/* 输入框和发送按钮 */}
        <div style={{ display: 'flex' }}>
          <TextArea
            rows={4}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onPressEnter={handleSend}
            placeholder="Type a message..."
          />
          <Button type="primary" onClick={handleSend} style={{ marginLeft: '8px' }}>
            Send
          </Button>
        </div>
      </div>
    </PageContainer>
  );
};

export default Chat;