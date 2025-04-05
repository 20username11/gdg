import React from 'react'
import Map from '../components/Map/Map'
import SideBar from '../components/Map/SideBar'

const SafeZoneFinder = () => {
  return (
    <div className='max-h-screen max-w-screen overflow-hidden'>
      <Map />
      {/* <SideBar /> */}
    </div>
  )
}

export default SafeZoneFinder
