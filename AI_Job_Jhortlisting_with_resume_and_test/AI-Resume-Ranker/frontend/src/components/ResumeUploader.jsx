import React, { useState } from "react";
import axios from "axios";
import { Upload, CheckCircle2, Star, TrendingUp, XCircle, Moon, Sun } from "lucide-react";

export default function ResumeRanker() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadedResumes, setUploadedResumes] = useState([]);
  const [topResumes, setTopResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true); // 🌙 default dark mode

  // Handle file selection
  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
  };

  // Handle upload
  const handleUpload = async () => {
    if (!selectedFiles.length) {
      alert("Please select at least one file!");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append("resumes", file));

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setUploadedResumes(res.data.uploaded_resumes || []);
      setTopResumes(res.data.top_resumes || []);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  // Toggle theme
  const toggleTheme = () => setDarkMode((prev) => !prev);

  // Dynamic theme classes
  const bgClass = darkMode
    ? "bg-black text-white"
    : "bg-gray-100 text-gray-900";

  const cardBg = darkMode
    ? "bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 border-gray-700"
    : "bg-white border-gray-300";

  const tableBorder = darkMode ? "border-gray-700" : "border-gray-300";

  return (
    <div className={`min-h-screen ${bgClass} transition-colors duration-500 p-8`}>
      <div className="max-w-7xl mx-auto relative">
        {/* THEME TOGGLE BUTTON */}
        <button
          onClick={toggleTheme}
          className={`absolute top-0 right-0 mt-4 mr-4 flex items-center justify-between w-16 h-8 rounded-full px-1 transition-all duration-500 ${
            darkMode
              ? "bg-gradient-to-r from-purple-600 to-indigo-600"
              : "bg-gradient-to-r from-yellow-300 to-yellow-500"
          }`}
        >
          <div
            className={`w-6 h-6 rounded-full bg-white shadow-md transform transition-transform duration-500 ${
              darkMode ? "translate-x-8" : "translate-x-0"
            }`}
          />
          {darkMode ? (
            <Moon size={18} className="absolute left-2 text-gray-200" />
          ) : (
            <Sun size={18} className="absolute right-2 text-yellow-700" />
          )}
        </button>

        {/* HEADER */}
        <h1 className="text-6xl font-bold text-center mb-12 bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
          AI Resume Ranker
        </h1>

        {/* UPLOAD SECTION */}
        <div className={`${cardBg} rounded-2xl p-8 mb-12 border shadow-2xl`}>
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-4">
              <label htmlFor="fileUpload">
                <span className="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg cursor-pointer">
                  Choose Files
                </span>
                <input
                  type="file"
                  id="fileUpload"
                  multiple
                  className="hidden"
                  onChange={handleFileChange}
                />
              </label>
              <span className={`${darkMode ? "text-gray-300" : "text-gray-600"}`}>
                {selectedFiles.length
                  ? `${selectedFiles.length} files selected`
                  : "No files selected"}
              </span>
            </div>

            <button
              onClick={handleUpload}
              disabled={loading || !selectedFiles.length}
              className={`px-8 py-3 rounded-xl font-semibold transition-all duration-300 transform flex items-center gap-2 shadow-lg ${
                loading || !selectedFiles.length
                  ? "bg-gray-600 cursor-not-allowed opacity-50"
                  : "bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 hover:scale-105"
              }`}
            >
              <Upload size={20} />
              {loading ? "Processing..." : "Upload"}
            </button>
          </div>
        </div>

        {/* YOUR UPLOADED RESUMES */}
        {uploadedResumes.length > 0 && (
          <div className="mb-12">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <TrendingUp className="text-cyan-400" />
              Your Uploaded Resumes
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              {uploadedResumes.map((resume, index) => (
                <div
                  key={index}
                  className={`rounded-xl p-6 border transition-all duration-300 shadow-xl ${
                    resume.rejected
                      ? `border-red-600 hover:border-red-400 ${
                          darkMode
                            ? "bg-gradient-to-br from-gray-900 to-gray-800 hover:shadow-red-400/20"
                            : "bg-red-50 hover:shadow-red-300/20"
                        }`
                      : `${cardBg} hover:border-cyan-500 hover:shadow-cyan-500/20`
                  }`}
                >
                  <div className="flex items-start gap-3 mb-4">
                    {resume.rejected ? (
                      <XCircle
                        className="text-red-400 mt-1 flex-shrink-0"
                        size={24}
                      />
                    ) : (
                      <CheckCircle2
                        className="text-green-400 mt-1 flex-shrink-0"
                        size={24}
                      />
                    )}
                    <h3
                      className={`text-xl font-semibold ${
                        darkMode ? "text-gray-100" : "text-gray-800"
                      }`}
                    >
                      {resume.name}
                    </h3>
                  </div>

                  {resume.rejected ? (
                    <p
                      className={`font-medium ml-7 ${
                        darkMode ? "text-red-400" : "text-red-600"
                      }`}
                    >
                      ❌ Rejected — Below required threshold
                    </p>
                  ) : (
                    <div className="space-y-3 ml-7">
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-medium ${
                            darkMode ? "text-gray-400" : "text-gray-600"
                          }`}
                        >
                          Score:
                        </span>
                        <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                          {resume.total_score?.toFixed(2)}
                        </span>
                      </div>

                      <div>
                        <span
                          className={`font-medium ${
                            darkMode ? "text-gray-400" : "text-gray-600"
                          }`}
                        >
                          Skills:
                        </span>
                        <span
                          className={`${
                            darkMode ? "text-gray-300" : "text-gray-700"
                          }`}
                        >
                          {resume.skills_found?.length
                            ? resume.skills_found
                            : "No skills detected"}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TOP RESUMES */}
        {topResumes.length > 0 && (
          <div>
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Star className="text-yellow-400 fill-yellow-400" />
              Top Resumes
            </h2>

            <div
              className={`rounded-2xl overflow-hidden border shadow-2xl ${
                darkMode
                  ? "bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 border-gray-700"
                  : "bg-white border-gray-300"
              }`}
            >
              <table className="w-full">
                <thead>
                  <tr
                    className={`border-b ${
                      darkMode
                        ? "border-gray-700 bg-gray-800/50"
                        : "border-gray-300 bg-gray-100"
                    }`}
                  >
                    <th className="text-left p-4 text-gray-400 font-semibold">
                      RANK
                    </th>
                    <th className="text-left p-4 text-gray-400 font-semibold">
                      NAME
                    </th>
                    <th className="text-left p-4 text-gray-400 font-semibold">
                      SCORE
                    </th>
                    <th className="text-left p-4 text-gray-400 font-semibold">
                      SKILLS
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {topResumes.map((resume, index) => (
                    <tr
                      key={resume.name + index}
                      className={`border-b ${
                        darkMode
                          ? "border-gray-800 hover:bg-gray-800/50"
                          : "border-gray-200 hover:bg-gray-100"
                      } transition-colors duration-200`}
                    >
                      <td className="p-4">
                        <div
                          className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg
                          ${
                            index === 0
                              ? "bg-gradient-to-br from-yellow-400 to-yellow-600 text-black"
                              : index === 1
                              ? "bg-gradient-to-br from-gray-400 to-gray-500 text-black"
                              : "bg-gradient-to-br from-orange-600 to-orange-700 text-white"
                          }`}
                        >
                          {index + 1}
                        </div>
                      </td>
                      <td
                        className={`p-4 font-medium ${
                          darkMode ? "text-gray-200" : "text-gray-800"
                        }`}
                      >
                        {resume.name}
                      </td>
                      <td className="p-4">
                        <span className="text-xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent">
                          {resume.total_score?.toFixed(3)}
                        </span>
                      </td>
                      <td
                        className={`p-4 text-sm ${
                          darkMode ? "text-gray-300" : "text-gray-700"
                        }`}
                      >
                        {resume.skills_found || resume.skills}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
