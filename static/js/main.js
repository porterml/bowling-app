// Main JavaScript for Bowling Analytics App

document.addEventListener("DOMContentLoaded", function () {
	// Initialize tooltips if Bootstrap is loaded
	if (typeof bootstrap !== "undefined") {
		var tooltipTriggerList = [].slice.call(
			document.querySelectorAll('[data-bs-toggle="tooltip"]')
		);
		var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
			return new bootstrap.Tooltip(tooltipTriggerEl);
		});
	}

	// Add fade-in animation to cards
	const cards = document.querySelectorAll(".card");
	cards.forEach((card, index) => {
		card.style.opacity = "0";
		card.style.transform = "translateY(20px)";

		setTimeout(() => {
			card.style.transition = "opacity 0.5s ease, transform 0.5s ease";
			card.style.opacity = "1";
			card.style.transform = "translateY(0)";
		}, index * 100);
	});

	// Auto-dismiss alerts after 5 seconds
	const alerts = document.querySelectorAll(".alert");
	alerts.forEach((alert) => {
		setTimeout(() => {
			if (alert.classList.contains("show")) {
				const bsAlert = new bootstrap.Alert(alert);
				bsAlert.close();
			}
		}, 5000);
	});
});

// Utility function to format numbers
function formatNumber(num) {
	return num.toLocaleString();
}

// Utility function to calculate percentage
function calculatePercentage(part, total) {
	if (total === 0) return 0;
	return Math.round((part / total) * 100);
}

// Function to validate frame scores
function validateFrameScore(score, isStrike, isSpare) {
	if (isStrike && score !== 10) {
		return "Strike frames must have a score of 10";
	}

	if (isSpare && score < 10) {
		return "Spare frames must have a score of at least 10";
	}

	if (score < 0 || score > 30) {
		return "Score must be between 0 and 30";
	}

	return null;
}

// Function to show validation errors
function showValidationError(element, message) {
	// Remove existing error
	const existingError = element.parentNode.querySelector(".validation-error");
	if (existingError) {
		existingError.remove();
	}

	// Add new error
	const errorDiv = document.createElement("div");
	errorDiv.className = "validation-error text-danger mt-1";
	errorDiv.innerHTML = `<small>${message}</small>`;
	element.parentNode.appendChild(errorDiv);

	// Add error styling to input
	element.classList.add("is-invalid");
}

// Function to clear validation errors
function clearValidationError(element) {
	const existingError = element.parentNode.querySelector(".validation-error");
	if (existingError) {
		existingError.remove();
	}
	element.classList.remove("is-invalid");
}

// Export functions for use in templates
window.BowlingApp = {
	formatNumber,
	calculatePercentage,
	validateFrameScore,
	showValidationError,
	clearValidationError,
};
