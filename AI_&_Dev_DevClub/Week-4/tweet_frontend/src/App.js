import React, { useState } from "react";
import axios from "axios";

function App() {
  const [generatedTweet, setGeneratedTweet] = useState("");
  const [predictedLikes, setPredictedLikes] = useState(null);

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
    try {
      const payload = {
        ...genForm,
        sentiment_target: genForm.sentiment_target / 10
      };
      const res = await axios.post("http://localhost:5001/generate", payload);
      setGeneratedTweet(res.data.generated_tweet);
    } catch (err) {
      setErrorGen("Failed to generate tweet.");
    } finally {
      setLoadingGen(false);
    }
  };

  const predictLikes = async () => {
    setLoadingPred(true);
    setErrorPred("");
    setPredictedLikes(null);
    try {
      const res = await axios.post("http://localhost:5000/predict", predForm);
      setPredictedLikes(res.data.predicted_likes);
    } catch (err) {
      setErrorPred("Failed to predict likes.");
    } finally {
      setLoadingPred(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-10">
        Tweet Generator & Like Predictor
      </h1>

      <div className="grid md:grid-cols-2 gap-10 max-w-6xl mx-auto">
        {/* Tweet Generator */}
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Generate Tweet</h2>
          <div className="space-y-4">
            <Input label="Company" name="company" value={genForm.company} onChange={handleGenChange} />
            <Checkbox label="Has Media" name="has_media" checked={genForm.has_media} onChange={handleGenChange} />
            <Input label="Sentiment (0-10)" name="sentiment_target" type="number" min={0} max={10} value={genForm.sentiment_target} onChange={handleGenChange} />
            <Select label="Brand Voice" name="brand_voice" value={genForm.brand_voice} onChange={handleGenChange} options={["Casual", "Professional", "Playful"]} />
            <Select label="Industry" name="industry" value={genForm.industry} onChange={handleGenChange} options={["Tech", "Food", "Fashion", "General"]} />
            <Textarea label="Message" name="message" value={genForm.message} onChange={handleGenChange} />
            <button
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
              onClick={generateTweet}
              disabled={loadingGen}
            >
              {loadingGen ? "Generating..." : "Generate Tweet"}
            </button>
            {errorGen && <p className="text-red-500">{errorGen}</p>}
            {generatedTweet && (
              <div className="p-4 bg-green-100 text-green-800 rounded">
                <strong>Generated Tweet:</strong> {generatedTweet}
              </div>
            )}
          </div>
        </div>

        {/* Likes Predictor */}
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Predict Likes</h2>
          <div className="space-y-4">
            <Select label="Day" name="day" value={predForm.day} onChange={handlePredChange} options={["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]} />
            <Input label="Hour (0–24)" name="hour" type="number" min={0} max={24} value={predForm.hour} onChange={handlePredChange} />
            <Input label="Username" name="username" value={predForm.username} onChange={handlePredChange} />
            <Input label="Company" name="company" value={predForm.company} onChange={handlePredChange} />
            <Checkbox label="Has Media" name="has_media" checked={predForm.has_media} onChange={handlePredChange} />
            <Textarea label="Content" name="content" value={predForm.content} onChange={handlePredChange} />
            <button
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded"
              onClick={predictLikes}
              disabled={loadingPred}
            >
              {loadingPred ? "Predicting..." : "Predict Likes"}
            </button>
            {errorPred && <p className="text-red-500">{errorPred}</p>}
            {predictedLikes !== null && (
              <div className="p-4 bg-yellow-100 text-yellow-800 rounded">
                <strong>Predicted Likes:</strong> {predictedLikes}
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