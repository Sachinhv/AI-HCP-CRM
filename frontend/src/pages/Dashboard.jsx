import Navbar from "../components/Navbar";
import InteractionForm from "../components/InteractionForm";
import AIChat from "../components/AIChat";

function Dashboard() {
  return (
    <>
      <Navbar />

      <div className="dashboard">

        <div className="left-panel">
          <InteractionForm />
        </div>

        <div className="right-panel">
          <AIChat />
        </div>

      </div>
    </>
  );
}

export default Dashboard;