import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import api from "../services/api";

import { addMessage } from "../redux/chatSlice";
import { updateInteraction } from "../redux/interactionSlice";

import ChatMessage from "./ChatMessage";

function AIChat() {

  const [message, setMessage] = useState("");

  const messages = useSelector((state) => state.chat.messages);

  const dispatch = useDispatch();

  const sendMessage = async () => {

    if (message.trim() === "") return;

    dispatch(
      addMessage({
        sender: "user",
        text: message,
      })
    );

    try {

      const response = await api.post("/chat/", {
        message: message,
      });

      dispatch(
        addMessage({
          sender: "assistant",
          text: JSON.stringify(response.data.result, null, 2),
        })
      );

      dispatch(updateInteraction(response.data.result));

      setMessage("");

    } catch (error) {

      dispatch(
        addMessage({
          sender: "assistant",
          text: JSON.stringify(response.data.result, null, 2),
        })
      );

      console.log(error);

    }

  };

  return (

    <div className="chat-container">

      <h2>AI Assistant</h2>

      <div className="chat-box">

        {messages.map((msg, index) => (

          <ChatMessage

            key={index}

            sender={msg.sender}

            text={msg.text}

          />

        ))}

      </div>

      <div className="chat-input">

        <input

          type="text"

          placeholder="Describe interaction..."

          value={message}

          onChange={(e) => setMessage(e.target.value)}

        />

        <button onClick={sendMessage}>

          Log

        </button>

      </div>

    </div>

  );

}

export default AIChat;