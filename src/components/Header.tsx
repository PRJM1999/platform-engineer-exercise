import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  const handleDashboardClick = () => {
    navigate("/");
  };

  return (
    <header className="bg-gray-800 text-white">
      <div className="container mx-auto p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">Platform Engineer Exercise</h1>
        <nav>
          <ul className="flex space-x-8">
            <li>
              <button
                className="hover:text-gray-300 px-4 py-2 text-sm"
                onClick={handleDashboardClick}
              >
                Dashboard
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;