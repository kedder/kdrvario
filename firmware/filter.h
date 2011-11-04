#ifndef filter_h
#define filter_h

class AlphaBetaFilter {
	private:
		float _alpha;
		float _beta;
		unsigned long _lastts;

		float _position;
		float _velocity;
		bool _initialized;

	public:
		AlphaBetaFilter(float alpha, float beta);
		void filter(long value);
		long getPosition();
		int getVelocity();
};

#endif
