import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { useNavigate, useParams } from 'react-router-dom';
import { interviewService } from '../services/interviewService';

const Report = () => {
  const navigate = useNavigate();
  const { sessionId: paramSessionId } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadReport();
  }, [paramSessionId]);

  const loadReport = async () => {
    try {
      if (paramSessionId) {
        // View historical report
        const data = await interviewService.getReportDetail(paramSessionId);
        setReport(data.report);
      } else {
        // Generate new report from current session
        const currentSessionId = sessionStorage.getItem('sessionId');
        if (!currentSessionId) {
          navigate('/upload-cv');
          return;
        }
        const response = await interviewService.generateReport(currentSessionId);
        setReport(response.report);
        
        // Clear session data after generation
        sessionStorage.removeItem('sessionId');
        sessionStorage.removeItem('questions');
        sessionStorage.removeItem('currentQuestion');
        sessionStorage.removeItem('responses');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load report');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Generating your performance report...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  if (!report) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold text-primary-900 mb-8 text-center">
          Performance Report
        </h1>

        {/* Summary Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold text-primary-800 mb-4">Summary</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-primary-50 rounded-lg">
              <p className="text-gray-600">Total Questions</p>
              <p className="text-3xl font-bold text-primary-900">{report.total_questions}</p>
            </div>
            <div className="p-4 bg-primary-50 rounded-lg">
              <p className="text-gray-600">Answers Received</p>
              <p className="text-3xl font-bold text-primary-900">{report.answers_received}</p>
            </div>
            <div className="p-4 bg-primary-50 rounded-lg">
              <p className="text-gray-600">Accuracy Level</p>
              <p className="text-3xl font-bold text-primary-900">{report.accuracy_level}</p>
            </div>
            <div className="p-4 bg-primary-50 rounded-lg">
              <p className="text-gray-600">Confidence Level</p>
              <p className="text-3xl font-bold text-primary-900">{report.confidence_level}</p>
            </div>
          </div>
        </div>

        {/* Detailed Responses Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold text-primary-800 mb-4">
            Detailed Analysis
          </h2>
          <div className="space-y-6">
            {report.detailed_responses.map((item, index) => (
              <div key={index} className="border-b border-gray-200 pb-6 last:border-b-0">
                <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-2 mb-2">
                  <p className="font-semibold text-gray-900 text-lg flex-1">
                    Question {index + 1}: {item.question}
                  </p>
                  {item.status && (
                    <span className={`px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap
                      ${item.status === 'Correct' ? 'bg-green-100 text-green-800' : 
                        item.status === 'Wrong' ? 'bg-red-100 text-red-800' : 
                        'bg-yellow-100 text-yellow-800'}`}>
                      {item.status} ({item.score !== undefined ? item.score : '-'})
                    </span>
                  )}
                </div>
                
                <div className="bg-gray-50 p-4 rounded-md mb-3">
                  <p className="text-sm text-gray-500 font-semibold mb-1">Your Answer:</p>
                  <p className="text-gray-700 whitespace-pre-wrap break-words">{item.candidate_answer || item.answer}</p>
                </div>

                {item.feedback && (
                   <div className="bg-blue-50 p-4 rounded-md border-l-4 border-blue-500">
                     <p className="text-sm text-blue-700 font-semibold mb-1">AI Feedback & Improvement:</p>
                     <p className="text-gray-700 whitespace-pre-wrap break-words">{item.feedback}</p>
                   </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Feedback Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold text-primary-800 mb-4">
            Personalized Feedback
          </h2>
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
            <article className="prose prose-sm md:prose-base lg:prose-lg max-w-none text-gray-800">
              <ReactMarkdown>{report.feedback}</ReactMarkdown>
            </article>
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={() => navigate('/profile')}
            className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors mr-4"
          >
            Back to Profile
          </button>
          <button
            onClick={() => navigate('/upload-cv')}
            className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
          >
            Start New Interview
          </button>
        </div>
      </div>
    </div>
  );
};

export default Report;

