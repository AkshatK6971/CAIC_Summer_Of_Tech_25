import React, { useState } from "react";
import axios from "axios";

const API_BASE = "https://tweet-intelligence-engine-backend.onrender.com";

function App() {
  const [generatedTweet, setGeneratedTweet] = useState("");
  const [generationInfo, setGenerationInfo] = useState({});
  const [predictedLikes, setPredictedLikes] = useState(null);
  const [popularityEstimate, setPopularityEstimate] = useState("");
  const [predictionDetails, setPredictionDetails] = useState({});

  const [genForm, setGenForm] = useState({
    company: "",
    has_media: false,
    sentiment_target: 5,
    brand_voice: "Casual",
    industry: "General",
    message: ""
  });

  const [predForm, setPredForm] = useState({
    day: "Monday",
    hour: 12,
    username: "",
    company: "",
    has_media: false,
    content: ""
  });

  const [loadingGen, setLoadingGen] = useState(false);
  const [loadingPred, setLoadingPred] = useState(false);
  const [errorGen, setErrorGen] = useState("");
  const [errorPred, setErrorPred] = useState("");

  const handleGenChange = (e) => {
    const { name, value, type, checked } = e.target;
    setGenForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  const handlePredChange = (e) => {
    const { name, value, type, checked } = e.target;
    setPredForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  const generateTweet = async () => {
    setLoadingGen(true);
    setErrorGen("");
    setGeneratedTweet("");
    setGenerationInfo({});
    try {
      const payload = {
        ...genForm,
        sentiment_target: genForm.sentiment_target / 10
      };
      const res = await axios.post(`${API_BASE}/generate`, payload);
      setGeneratedTweet(res.data.generated_tweet);
      setGenerationInfo(res.data.info || {});
    } catch (err) {
      setErrorGen("❌ Failed to generate tweet.");
    } finally {
      setLoadingGen(false);
    }
  };

  const predictLikes = async () => {
    setLoadingPred(true);
    setErrorPred("");
    setPredictedLikes(null);
    setPopularityEstimate("");
    setPredictionDetails({});
    try {
      const res = await axios.post(`${API_BASE}/predict`, predForm);
      setPredictedLikes(res.data.predicted_likes);
      setPopularityEstimate(res.data.popularity_estimate || "");
      setPredictionDetails(res.data.details || {});
    } catch (err) {
      setErrorPred("❌ Failed to predict likes.");
    } finally {
      setLoadingPred(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-10">
        🚀 Tweet Generator & Like Predictor 📊
      </h1>

      <div className="grid md:grid-cols-2 gap-10 max-w-6xl mx-auto">
        
        {/* Tweet Generator */}
        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Generate Tweet</h2>
          <div className="space-y-4">
            <Input label="Company" name="company" value={genForm.company} onChange={handleGenChange} />
            <Checkbox label="Has Media" name="has_media" checked={genForm.has_media} onChange={handleGenChange} />
            <Input label="Sentiment (0-10)" name="sentiment_target" type="number" min={0} max={10} value={genForm.sentiment_target} onChange={handleGenChange} />
            <Select label="Brand Voice" name="brand_voice" value={genForm.brand_voice} onChange={handleGenChange} options={["Casual", "Professional", "Playful"]} />
            <Select label="Industry" name="industry" value={genForm.industry} onChange={handleGenChange} options={["Tech", "Food", "Fashion", "General"]} />
            <Textarea label="Message" name="message" value={genForm.message} onChange={handleGenChange} />
            <button
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
              onClick={generateTweet}
              disabled={loadingGen}
            >
              {loadingGen ? "Generating..." : "Generate Tweet"}
            </button>

            {errorGen && <p className="text-red-500 font-semibold">{errorGen}</p>}

            {generatedTweet && (
              <div className="p-5 bg-green-50 text-green-900 rounded-xl shadow-md border border-green-200 space-y-3">
                <p className="text-lg font-bold">🎉 Generated Tweet:</p>
                <p className="text-base">{generatedTweet}</p>

                {Object.keys(generationInfo).length > 0 && (
                  <div className="text-sm text-green-700">
                    <p className="font-semibold">Info:</p>
                    <div className="pl-3 border-l-4 border-green-300 space-y-1 font-mono text-green-800">
                      {Object.entries(generationInfo).map(([key, value]) => (
                        <div key={key}>
                          <span className="font-bold">{key}:</span> {value}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Likes Predictor */}
        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Predict Likes</h2>
          <div className="space-y-4">
            <Select label="Day" name="day" value={predForm.day} onChange={handlePredChange} options={["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]} />
            <Input label="Hour (0–24)" name="hour" type="number" min={0} max={24} value={predForm.hour} onChange={handlePredChange} />
            <Input label="Username" name="username" value={predForm.username} onChange={handlePredChange} />
            <Input label="Company" name="company" value={predForm.company} onChange={handlePredChange} />
            <Checkbox label="Has Media" name="has_media" checked={predForm.has_media} onChange={handlePredChange} />
            <Textarea label="Content" name="content" value={predForm.content} onChange={handlePredChange} />
            <button
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-lg transition"
              onClick={predictLikes}
              disabled={loadingPred}
            >
              {loadingPred ? "Predicting..." : "Predict Likes"}
            </button>

            {errorPred && <p className="text-red-500 font-semibold">{errorPred}</p>}

            {predictedLikes !== null && (
              <div className="p-5 bg-yellow-50 text-yellow-900 rounded-xl shadow-md border border-yellow-200 space-y-3">
                <p className="text-lg font-bold">📊 Predicted Likes: {predictedLikes}</p>
                {popularityEstimate && (
                  <p className="text-xl font-semibold">{popularityEstimate}</p>
                )}

                {Object.keys(predictionDetails).length > 0 && (
                  <div className="text-sm text-yellow-700">
                    <p className="font-semibold">Details:</p>
                    <div className="pl-3 border-l-4 border-yellow-300 space-y-1 font-mono text-yellow-800">
                      {Object.entries(predictionDetails).map(([key, value]) => (
                        <div key={key}>
                          <span className="font-bold">{key}:</span> {String(value)}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

// Reusable form components
const Input = ({ label, ...props }) => (
  <label className="block">
    <span className="text-gray-600">{label}</span>
    <input className="mt-1 w-full px-3 py-2 border rounded" {...props} />
  </label>
);

const Select = ({ label, options, ...props }) => (
  <label className="block">
    <span className="text-gray-600">{label}</span>
    <select className="mt-1 w-full px-3 py-2 border rounded" {...props}>
      {options.map((opt) => (
        <option key={opt} value={opt}>{opt}</option>
      ))}
    </select>
  </label>
);

const Textarea = ({ label, ...props }) => (
  <label className="block">
    <span className="text-gray-600">{label}</span>
    <textarea className="mt-1 w-full px-3 py-2 border rounded" rows={3} {...props} />
  </label>
);

const Checkbox = ({ label, ...props }) => (
  <label className="inline-flex items-center space-x-2">
    <input type="checkbox" className="form-checkbox" {...props} />
    <span className="text-gray-600">{label}</span>
  </label>
);

export default App;
