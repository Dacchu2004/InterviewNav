import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { interviewService } from '../services/interviewService';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await interviewService.getProfile();
      setProfile(data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading profile...</p>
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

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold text-primary-900 mb-8">
          {profile?.user?.username}'s Profile
        </h1>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold text-primary-800 mb-4">
            Personal Information
          </h2>
          <div className="space-y-2">
            <p className="text-gray-700">
              <span className="font-semibold">Email:</span> {profile?.user?.email}
            </p>
            <p className="text-gray-700">
              <span className="font-semibold">Account Status:</span>{' '}
              <span className={profile?.user?.is_active ? 'text-green-600' : 'text-red-600'}>
                {profile?.user?.is_active ? 'Active' : 'Inactive'}
              </span>
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold text-primary-800 mb-4">
            Your CVs
          </h2>
          {profile?.cvs && profile.cvs.length > 0 ? (
            <ul className="space-y-2">
              {profile.cvs.map((cv) => (
                <li
                  key={cv.id}
                  className="border-b border-gray-200 pb-2 last:border-b-0"
                >
                  <p className="text-gray-700">
                    <span className="font-semibold">{cv.company_name}</span> - {cv.job_role} |{' '}
                    <span className="text-primary-600">Level: {cv.interview_level}</span>
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-600">No CVs uploaded yet.</p>
          )}
        </div>

        <Link
          to="/upload-cv"
          className="inline-block bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          Upload New CV
        </Link>
      </div>
    </div>
  );
};

export default Profile;

