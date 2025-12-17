import { Link } from 'react-router-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHouse, faUtensils, faUser, faRightToBracket, faRightFromBracket } from '@fortawesome/free-solid-svg-icons'

import './style.css'

export const Navbar = () => {
    return (
        <nav className='navBar'>
            <ul className='navBar-list'>
                <li className='navBar-item'>
                    <Link to="/">
                        <FontAwesomeIcon icon={faHouse} />
                        Home
                    </Link>
                </li>
                <li className='navBar-item'>
                    <Link to="/restaurants">
                        <FontAwesomeIcon icon={faUtensils} />
                        Restaurants
                    </Link>
                </li>
                <li className='navBar-item'>
                    <Link to="/users">
                        <FontAwesomeIcon icon={faUser} />
                        Users
                    </Link>
                </li>
                <li className='navBar-item'>
                    <Link to="/login">
                        <FontAwesomeIcon icon={faRightToBracket} />
                        Login
                    </Link>
                </li>
                <li className='navBar-item'>
                    <Link to="/logout">
                        <FontAwesomeIcon icon={faRightFromBracket} />
                        Logout
                    </Link>
                </li>
            </ul>
        </nav>
    )
}