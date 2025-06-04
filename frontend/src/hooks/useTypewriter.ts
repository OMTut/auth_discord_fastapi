import { useState, useEffect } from 'react';

interface UseTypewriterOptions {
  text: string;
  speed?: number; // milliseconds per character
  cursorBlinkRate?: number; // milliseconds per blink
}

interface UseTypewriterReturn {
  displayedText: string;
  isTyping: boolean;
  showCursor: boolean;
}

export const useTypewriter = ({
  text,
  speed = 50,
  cursorBlinkRate = 500
}: UseTypewriterOptions): UseTypewriterReturn => {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showCursor, setShowCursor] = useState(true);

  // Typewriter effect
  useEffect(() => {
    if (!text) {
      setDisplayedText('');
      setIsTyping(false);
      return;
    }

    setDisplayedText('');
    setIsTyping(true);
    let index = 0;
    
    const typeTimer = setInterval(() => {
      if (index < text.length) {
        setDisplayedText(text.substring(0, index + 1));
        index++;
      } else {
        setIsTyping(false);
        clearInterval(typeTimer);
      }
    }, speed);

    return () => clearInterval(typeTimer);
  }, [text, speed]);

  // Blinking cursor effect
  useEffect(() => {
    const cursorTimer = setInterval(() => {
      setShowCursor(prev => !prev);
    }, cursorBlinkRate);

    return () => clearInterval(cursorTimer);
  }, [cursorBlinkRate]);

  return {
    displayedText,
    isTyping,
    showCursor
  };
};

