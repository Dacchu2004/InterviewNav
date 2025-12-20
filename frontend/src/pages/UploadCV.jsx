import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { interviewService } from '../services/interviewService';

const UploadCV = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    cv_file: null,
    company_name: '',
    job_role: '',
    interview_level: 'Beginner',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    if (e.target.name === 'cv_file') {
      setFormData({
        ...formData,
        cv_file: e.target.files[0],
      });
    } else {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value,
      });
    }
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.cv_file) {
      setError('Please select a CV file');
      return;
    }

    setLoading(true);

    try {
      const uploadFormData = new FormData();
      uploadFormData.append('cv_file', formData.cv_file);
      uploadFormData.append('company_name', formData.company_name);
      uploadFormData.append('job_role', formData.job_role);
      uploadFormData.append('interview_level', formData.interview_level);

      const response = await interviewService.uploadCV(uploadFormData);
      
      // Store session ID and questions in sessionStorage
      sessionStorage.setItem('sessionId', response.session_id);
      sessionStorage.setItem('questions', JSON.stringify(response.questions));
      sessionStorage.setItem('currentQuestion', '0');
      sessionStorage.setItem('responses', JSON.stringify([]));

      navigate('/interview');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload CV. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="container mx-auto max-w-2xl">
        <h1 className="text-4xl font-bold text-primary-900 mb-8 text-center">
          Upload Your CV
        </h1>

        <div className="bg-white rounded-lg shadow-md p-8">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="cv_file"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Upload CV (PDF or DOCX)
              </label>
              <input
                type="file"
                id="cv_file"
                name="cv_file"
                accept=".pdf,.docx"
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <p className="mt-2 text-sm text-gray-500">
                Allowed file types: PDF, DOCX (max size: 5MB)
              </p>
            </div>

            <div>
              <label
                htmlFor="company_name"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Company Name
              </label>
              <input
                type="text"
                id="company_name"
                name="company_name"
                value={formData.company_name}
                onChange={handleChange}
                required
                maxLength={50}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <div>
              <label
                htmlFor="job_role"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Job Role
              </label>
              <input
                type="text"
                id="job_role"
                name="job_role"
                value={formData.job_role}
                onChange={handleChange}
                required
                maxLength={50}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <div>
              <label
                htmlFor="interview_level"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Interview Level
              </label>
              <select
                id="interview_level"
                name="interview_level"
                value={formData.interview_level}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Uploading and Processing...' : 'Upload CV'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UploadCV;

