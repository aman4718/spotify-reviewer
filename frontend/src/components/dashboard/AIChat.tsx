"use client"
import React, { useState } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Send, Bot, User } from 'lucide-react'
import { chatWithAssistant } from '@/lib/api'

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function AIChat() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am the Spotify AI Product Assistant. Ask me anything about the user reviews!' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const response = await chatWithAssistant(userMsg);
      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error connecting to AI Assistant." }]);
    } finally {
      setLoading(false);
    }
  }

  const suggestions = [
    "What are the biggest complaints from Free tier users?",
    "Summarize the high priority bugs.",
    "Are there any UI or widget-related requests?"
  ];

  const handleSuggestionClick = async (text: string) => {
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setLoading(true);
    try {
      const response = await chatWithAssistant(text);
      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error connecting to AI Assistant." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="flex flex-col h-[600px] bg-black/40 border-green-900/50 backdrop-blur-xl">
      <CardHeader className="border-b border-white/10 pb-4">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Bot className="text-green-500" /> AI Product Assistant
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center shrink-0">
                <Bot size={16} className="text-green-500" />
              </div>
            )}
            <div className={`p-3 rounded-2xl max-w-[80%] text-sm whitespace-pre-wrap ${msg.role === 'user' ? 'bg-green-600 text-white rounded-tr-sm' : 'bg-white/10 text-gray-200 rounded-tl-sm'}`}>
              {msg.content}
            </div>
            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center shrink-0">
                <User size={16} className="text-blue-400" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex gap-3 justify-start">
            <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center shrink-0">
              <Bot size={16} className="text-green-500" />
            </div>
            <div className="p-3 rounded-2xl bg-white/10 text-gray-400 text-sm italic rounded-tl-sm">
              Thinking...
            </div>
          </div>
        )}
      </CardContent>

      <div className="px-4 pb-2 pt-0 flex flex-wrap gap-2">
        {suggestions.map((sugg, idx) => (
          <button 
            key={idx}
            onClick={() => handleSuggestionClick(sugg)}
            disabled={loading}
            className="text-xs bg-white/5 hover:bg-green-500/20 text-green-300 border border-green-500/20 px-3 py-1.5 rounded-full transition-colors disabled:opacity-50"
          >
            {sugg}
          </button>
        ))}
      </div>

      <div className="p-4 border-t border-white/10 flex gap-2">
        <input 
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="e.g., What is the top feature request?"
          className="flex-1 bg-white/5 border border-white/10 rounded-full px-4 py-2 text-sm focus:outline-none focus:border-green-500 transition-colors text-white"
        />
        <button 
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center hover:bg-green-400 disabled:opacity-50 transition-colors shrink-0"
        >
          <Send size={16} className="text-black ml-[-2px]" />
        </button>
      </div>
    </Card>
  )
}
