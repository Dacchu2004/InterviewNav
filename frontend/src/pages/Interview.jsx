import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { interviewService } from '../services/interviewService';
import { SpeechRecognitionHelper, speakText } from '../utils/speechRecognition';

const Interview = () => {
  const navigate = useNavigate();
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState('');
  const [progress, setProgress] = useState(0);
  const [total, setTotal] = useState(0);
  const [answer, setAnswer] = useState('');
  const [interimAnswer, setInterimAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [completed, setCompleted] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    // Initialize session from sessionStorage
    const storedSessionId = sessionStorage.getItem('sessionId');
    if (!storedSessionId) {
      navigate('/upload-cv');
      return;
    }

    setSessionId(storedSessionId);
    loadCurrentQuestion(storedSessionId);

    // Initialize speech recognition
    try {
      recognitionRef.current = new SpeechRecognitionHelper();
      recognitionRef.current.setOnResult((final, interim) => {
        setAnswer(final);
        setInterimAnswer(interim);
      });
      recognitionRef.current.setOnError((error) => {
        console.error('Speech recognition error:', error);
        setIsListening(false);
      });
    } catch (err) {
      console.error('Speech recognition not supported:', err);
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [navigate]);

  const loadCurrentQuestion = async (sid) => {
    try {
      const response = await interviewService.getCurrentQuestion(sid);
      
      if (response.completed) {
        setCompleted(true);
        return;
      }

      setQuestion(response.question);
      setProgress(response.progress);
      setTotal(response.total);

      // Speak the question automatically
      speakText(response.question);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load question');
    }
  };

  const handleStartSpeaking = () => {
    if (recognitionRef.current) {
      setAnswer('');
      setInterimAnswer('');
      recognitionRef.current.start();
      setIsListening(true);
    } else {
      setError('Speech recognition is not supported in your browser');
    }
  };

  const handleStop = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  const handleSubmit = async () => {
    if (!answer.trim()) {
      setError('Please provide an answer before submitting');
      return;
    }

    if (!sessionId) {
      setError('Session not found');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await interviewService.submitAnswer(sessionId, answer);

      if (response.completed) {
        // Navigate to report generation
        navigate('/report');
      } else {
        // Load next question
        setQuestion(response.next_question);
        setProgress(response.progress);
        setTotal(response.total);
        setAnswer('');
        setInterimAnswer('');
        // Speak next question
        speakText(response.next_question);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit answer');
    } finally {
      setLoading(false);
      handleStop();
    }
  };

  if (completed) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-primary-900 mb-4">
            Interview Completed!
          </h2>
          <button
            onClick={() => navigate('/report')}
            className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            View Report
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <div className="mb-6">
          <p className="text-lg text-gray-600">
            Question {progress} of {total}
          </p>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-primary-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${(progress / total) * 100}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8 mb-6">
          <h2 id="question-text" className="text-2xl font-semibold text-primary-900 mb-6">
            {question}
          </h2>

          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-700 mb-2">Your Answer:</h3>
            <div className="min-h-[150px] p-4 border border-gray-300 rounded-lg bg-gray-50">
              <p className="text-gray-800 whitespace-pre-wrap">
                {answer}
                <span className="text-gray-500">{interimAnswer}</span>
              </p>
              {!answer && !interimAnswer && (
                <p className="text-gray-400 italic">Your transcribed answer will appear here...</p>
              )}
            </div>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <div className="flex space-x-4">
            <button
              type="button"
              onClick={handleStartSpeaking}
              disabled={isListening || loading}
              className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-colors ${
                isListening
                  ? 'bg-yellow-500 hover:bg-yellow-600 text-white'
                  : 'bg-primary-600 hover:bg-primary-700 text-white'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {isListening ? '🎤 Listening...' : '🎤 Start Speaking'}
            </button>
            <button
              type="button"
              onClick={handleStop}
              disabled={!isListening}
              className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Stop
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading || !answer.trim()}
              className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Submitting...' : 'Submit Answer'}
            </button>
          </div>

          <p className="mt-4 text-sm text-gray-500 text-center">
            Click "Start Speaking" to answer. Click "Submit Answer" when you're done.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Interview;

