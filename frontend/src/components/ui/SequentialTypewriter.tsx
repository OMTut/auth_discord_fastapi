import React, { useState, useEffect } from 'react';
import TypewriterText from './TypewriterText';

interface SequentialTypewriterProps {
  paragraphs: string[];
  speed?: number;
  cursorBlinkRate?: number;
  cursorChar?: string;
  delayBetween?: number; // delay between paragraphs in ms
  className?: string;
}

const SequentialTypewriter: React.FC<SequentialTypewriterProps> = ({
  paragraphs,
  speed = 50,
  cursorBlinkRate = 500,
  cursorChar = '_',
  delayBetween = 1000,
  className
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [completedParagraphs, setCompletedParagraphs] = useState<string[]>([]);
  const [isComplete, setIsComplete] = useState(false);

  // Move to next paragraph after current one finishes typing
  useEffect(() => {
    if (currentIndex < paragraphs.length) {
      const currentText = paragraphs[currentIndex];
      const typingTime = currentText.length * speed + delayBetween;
      
      const timer = setTimeout(() => {
        setCompletedParagraphs(prev => [...prev, currentText]);
        setCurrentIndex(prev => prev + 1);
        
        if (currentIndex + 1 >= paragraphs.length) {
          setIsComplete(true);
        }
      }, typingTime);

      return () => clearTimeout(timer);
    }
  }, [currentIndex, paragraphs, speed, delayBetween]);

  return (
    <div className={className}>
      {/* Render completed paragraphs */}
      {completedParagraphs.map((paragraph, index) => (
        <p key={index}>{paragraph}</p>
      ))}
      
      {/* Render currently typing paragraph */}
      {currentIndex < paragraphs.length && (
        <p>
          <TypewriterText
            text={paragraphs[currentIndex]}
            speed={speed}
            cursorBlinkRate={cursorBlinkRate}
            cursorChar={isComplete ? '' : cursorChar}
          />
        </p>
      )}
    </div>
  );
};

export default SequentialTypewriter;

