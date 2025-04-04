import React from 'react'
// import Map from '../components/Map/Map'
import GradientButton from '../components/Button/GradientButton'
import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className='h-[100vh] flex justify-center items-center bg-gradient-to-b from-black to-gray-900 text-white text-center py-20 px-4 '>
       <div className="">
      <h1 className="text-5xl md:text-6xl font-bold">
      Find a Safe Place to Live <br /> &  <br /> <span className="text-gray-400">Know Your Rights</span>
      </h1>
      <p className="text-lg md:text-xl text-gray-300 mt-4 max-w-2xl mx-auto">
      AI-powered safety insights and legal guidance for women, ensuring security and empowerment at every step.
      </p>
    <div className="flex justify-center gap-10 mt-12">
      <Link to="/safeZone">
        <GradientButton text="Safety Insights" />
      </Link>
      <Link to="/findRoute">
        <GradientButton text="Find best Route" />
      </Link>
    </div>
    </div>
    {/* <Map/> */}
    </div>
  )
}

export default Home
