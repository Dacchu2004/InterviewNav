import { Link } from 'react-router-dom';
import { authService } from '../services/authService';

const Home = () => {
  const isAuthenticated = authService.isAuthenticated();

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-primary-900 mb-6">
            Welcome to Virtual Interview Navigator
          </h1>
          <p className="text-xl text-gray-700 mb-8">
            Prepare for your interviews with AI-powered personalized questions and real-time feedback
          </p>
          <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
            <h2 className="text-2xl font-semibold text-primary-800 mb-4">
              How It Works
            </h2>
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div className="p-4">
                <div className="text-3xl font-bold text-primary-600 mb-2">1</div>
                <h3 className="font-semibold mb-2">Upload Your CV</h3>
                <p className="text-gray-600">
                  Upload your resume and specify the company and role you're applying for
                </p>
              </div>
              <div className="p-4">
                <div className="text-3xl font-bold text-primary-600 mb-2">2</div>
                <h3 className="font-semibold mb-2">Answer Questions</h3>
                <p className="text-gray-600">
                  Practice answering personalized interview questions using voice input
                </p>
              </div>
              <div className="p-4">
                <div className="text-3xl font-bold text-primary-600 mb-2">3</div>
                <h3 className="font-semibold mb-2">Get Feedback</h3>
                <p className="text-gray-600">
                  Receive AI-powered feedback to improve your interview performance
                </p>
              </div>
            </div>
          </div>
          {isAuthenticated ? (
            <Link
              to="/upload-cv"
              className="inline-block bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors text-lg"
            >
              Start Interview Preparation
            </Link>
          ) : (
            <div className="space-x-4">
              <Link
                to="/signup"
                className="inline-block bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors text-lg"
              >
                Get Started
              </Link>
              <Link
                to="/login"
                className="inline-block bg-white hover:bg-gray-100 text-primary-600 font-semibold py-3 px-8 rounded-lg border-2 border-primary-600 transition-colors text-lg"
              >
                Login
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;

