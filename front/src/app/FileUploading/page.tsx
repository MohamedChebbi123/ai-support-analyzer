'use client';
import React, { useState } from 'react';

const Page = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    } else {
      setFile(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); 

    setLoading(true);

    const formData = new FormData();
    if (file) {
      formData.append('file', file);
    } else {
      setMessage("Please select a file to upload.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      setMessage(result.message || "File processed successfully");
      console.log(result);
    } catch (error) {
      setMessage("Failed to upload file");
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          CSV File Upload
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Upload your data file for processing
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Upload your CSV file
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div className="space-y-1 text-center">
                  <input
                    id="fileuploaded"
                    name="fileuploaded"
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    required
                    className="text-sm text-gray-600"
                  />
                  <p className="text-xs text-gray-500">CSV files up to 10MB</p>
                </div>
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
              >
                {loading ? 'Processing...' : 'Process File'}
              </button>
              <p className="mt-2 text-center text-sm text-gray-700">{message}</p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Page;
