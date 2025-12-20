import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { interviewService } from '../services/interviewService';

const Report = () => {
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    generateReport();
  }, []);

  const generateReport = async () => {
    const sessionId = sessionStorage.getItem('sessionId');
    if (!sessionId) {
      navigate('/upload-cv');
      return;
    }

    try {
      const response = await interviewService.generateReport(sessionId);
      setReport(response.report);
      
      // Clear session data
      sessionStorage.removeItem('sessionId');
      sessionStorage.removeItem('questions');
      sessionStorage.removeItem('currentQuestion');
      sessionStorage.removeItem('responses');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate report');
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
            Detailed Responses
          </h2>
          <div className="space-y-6">
            {report.detailed_responses.map((item, index) => (
              <div key={index} className="border-b border-gray-200 pb-4 last:border-b-0">
                <p className="font-semibold text-gray-900 mb-2">
                  Question {index + 1}: {item.question}
                </p>
                <p className="text-gray-700 ml-4">{item.answer}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Feedback Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold text-primary-800 mb-4">
            Personalized Feedback
          </h2>
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <pre className="whitespace-pre-wrap text-gray-800 font-sans">
              {report.feedback}
            </pre>
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

