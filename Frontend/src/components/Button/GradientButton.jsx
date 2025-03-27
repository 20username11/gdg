import React from "react";

const GradientButton = (props) => {
  return (
    <button className="px-6 py-3 hover:scale-110 text-white font-semibold rounded-lg bg-gradient-to-r from-blue-400 to-purple-500 shadow-md hover:from-blue-500 hover:to-purple-600 transition-all">
      {props.text}
    </button>
  );
};

export default GradientButton;
