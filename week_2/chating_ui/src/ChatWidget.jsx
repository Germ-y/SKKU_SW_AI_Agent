import React, { useState } from "react";
import "./ChatWidget.css";

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { from: "bot", text: "안녕하세요. 무엇을 도와드릴까요?" },
  ]);
  const [input, setInput] = useState("");

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { from: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: "문의 내용을 확인했습니다. 잠시만 기다려 주세요." },
      ]);
    }, 500);
  };

  return (
    <>
      <button className="chat-toggle-btn" onClick={toggleChat}>❓</button>

      {isOpen && (
        <div className="chat-widget">
          <div className="chat-header">
            <span>트로스트 고객센터</span>
            <button onClick={toggleChat}>✖</button>
          </div>
          <div className="chat-body">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.from}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="메시지를 입력하세요..."
            />
            <button onClick={sendMessage}>전송</button>
          </div>
        </div>
      )}
    </>
  );
}
