import { useSelector } from "react-redux";

const INTERACTION_TYPES = ["Meeting", "Call", "Email", "Conference"];
const SENTIMENTS = ["Positive", "Neutral", "Negative"];

// NOTE: This form is READ-ONLY BY DESIGN.
// The rep never types into these fields directly. All values here are
// populated exclusively by the LangGraph agent's `log_interaction` and
// `edit_interaction` tools (via AIChat.jsx dispatching `updateInteraction`
// into Redux). This mirrors a real AI-first CRM workflow: the rep describes
// the interaction in natural language on the right, and the agent extracts
// + fills + saves the structured record on the left.
function InteractionForm() {
  const interaction = useSelector((state) => state.interaction);

  const hasData = Boolean(
    interaction.hcp_name || interaction.topics_discussed || interaction.id
  );

  return (
    <div className="form-card">
      <h2>Interaction Details</h2>

      <div className="ai-status-banner">
        {interaction.id ? (
          <span className="save-msg success">
            ✅ Saved to CRM (Interaction #{interaction.id})
          </span>
        ) : hasData ? (
          <span className="save-msg pending">
            ✍️ Draft from AI Assistant — not yet confirmed
          </span>
        ) : (
          <span className="save-msg idle">
            Waiting for the AI Assistant to log this interaction...
          </span>
        )}
      </div>

      <div className="row">
        <div className="form-group">
          <label>HCP Name</label>
          <input
            type="text"
            placeholder="Filled by AI Assistant..."
            value={interaction.hcp_name}
            readOnly
          />
        </div>

        <div className="form-group">
          <label>Interaction Type</label>
          <select value={interaction.interaction_type} disabled>
            {INTERACTION_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="row">
        <div className="form-group">
          <label>Date</label>
          <input type="date" value={interaction.date} readOnly disabled />
        </div>

        <div className="form-group">
          <label>Time</label>
          <input type="time" value={interaction.time} readOnly disabled />
        </div>
      </div>

      <div className="form-group">
        <label>Attendees</label>
        <textarea
          rows="2"
          placeholder="Filled by AI Assistant..."
          value={interaction.attendees}
          readOnly
        />
      </div>

      <div className="form-group">
        <label>Topics Discussed</label>
        <textarea
          rows="4"
          placeholder="Filled by AI Assistant..."
          value={interaction.topics_discussed}
          readOnly
        />
      </div>

      <div className="row">
        <div className="form-group">
          <label>Materials Shared</label>
          <input
            placeholder="No materials added"
            value={interaction.materials_shared}
            readOnly
          />
        </div>

        <div className="form-group">
          <label>Samples Distributed</label>
          <input
            placeholder="No samples added"
            value={interaction.samples_distributed}
            readOnly
          />
        </div>
      </div>

      <div className="form-group">
        <label>Observed/Inferred HCP Sentiment</label>
        <div className="sentiment-row">
          {SENTIMENTS.map((s) => (
            <label key={s} className="radio-option">
              <input
                type="radio"
                name="sentiment"
                value={s}
                checked={interaction.sentiment === s}
                disabled
                readOnly
              />
              {s}
            </label>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>Outcomes</label>
        <textarea
          rows="3"
          placeholder="Filled by AI Assistant..."
          value={interaction.outcomes}
          readOnly
        />
      </div>

      <div className="form-group">
        <label>Follow-up Actions</label>
        <textarea
          rows="3"
          placeholder="Filled by AI Assistant..."
          value={interaction.follow_up}
          readOnly
        />
      </div>
    </div>
  );
}

export default InteractionForm;
