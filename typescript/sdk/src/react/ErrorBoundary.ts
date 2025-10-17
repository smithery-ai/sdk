import { Component, createElement, type ReactNode } from "react"

interface ErrorBoundaryProps {
	children: ReactNode
	fallback?: (error: Error) => ReactNode
}

interface ErrorBoundaryState {
	hasError: boolean
	error: Error | null
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {

	constructor(props: ErrorBoundaryProps) {
		super(props)
		this.state = { hasError: false, error: null }
	}

	static getDerivedStateFromError(error: Error): ErrorBoundaryState {
		return { hasError: true, error }
	}

	componentDidCatch(error: Error, errorInfo: { componentStack?: string }) {
		console.error("Widget error:", error, errorInfo)
	}

	render() {
		if (this.state.hasError && this.state.error) {
			if (this.props.fallback) {
				return this.props.fallback(this.state.error)
			}

			return createElement(
				"div",
				{
					style: {
						padding: "16px",
						color: "#d32f2f",
						fontFamily: "system-ui, sans-serif",
					},
				},
				createElement(
					"h3",
					{ style: { margin: "0 0 8px 0", fontSize: "14px" } },
					"Widget Error",
				),
				createElement(
					"p",
					{ style: { margin: "0", fontSize: "12px", opacity: 0.8 } },
					this.state.error.message || "An error occurred",
				),
			)
		}

		return this.props.children
	}
}
