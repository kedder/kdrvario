function k = make_kalman(Q, R, A, H, xhat, P)
	k.Q = Q;
	k.R = R;
	k.A = A;
	k.H = H;
	k.xhat = xhat;
	k.P = P;
	k.I = eye(rows(Q));
endfunction

function flt = kalman (flt, z)
	% Kalman filter implementation

	flt.xhatminus = flt.A * flt.xhat;
	Pminus = flt.A * flt.P * flt.A' + flt.Q;

	K = Pminus * flt.H' * ( flt.H * Pminus * flt.H' + flt.R )^-1;
	flt.xhat = flt.xhatminus + K * (z - flt.H * flt.xhatminus);
	flt.P = (flt.I - (K * flt.H)) * Pminus;
endfunction

function alt = pressure_to_alt(pressure)
	STD_PRESSURE = 101325;
	if (isscalar(pressure))
		alt = 44330 * (1 - (pressure/STD_PRESSURE) ^ (1/5.255));
	else
		alt = [];
		for p = pressure'
			a = pressure_to_alt(p);
            alt = [alt; pressure_to_alt(p)];
		endfor
	endif
endfunction

function filtered = filter_with_kalman(flt, data)
	filtered = [];
	for z = data'
		flt = kalman(flt, z);
		filtered = [filtered; flt.xhat']; % flt.xhat(2)];
	endfor
endfunction

function filtered = test_kalman_2d(data, dt, q, r, x0)
	Q = [(dt^4)/4, (dt^3)/2; (dt^3)/2, dt^2] * q;  % process covariance
	R = r;  % measurement covarience
	A = [1, dt; 0, 1]
	H = [1, 0];

	% Initial state
	xhat = [x0; 0];
	P = Q * 100;

	flt = make_kalman(Q, R, A, H, xhat, P);
	filtered = filter_with_kalman(flt, data);
endfunction

function filtered = test_kalman_1d(data, dt, q, r, x0)
	Q = dt * q;
	R = r;
	A = 1;
	H = 1;
	xhat = x0;
	P = Q;

	flt = make_kalman(Q, R, A, H, xhat, P);
	filtered = filter_with_kalman(flt, data);
endfunction

% Load data
load altchange.mat
data = pressure_to_alt(data);
% Basic filter for KDR vario sampled data

dt = 1/30;
q = 115.400;  % process variance
r = 0.43;   % measurement variance
x0 = 36;

% perform tests
k2d = test_kalman_2d(data, dt, q, r, x0);
k1d = test_kalman_1d(data, dt, 0.04, r, x0);


% plot data
timeline = (0:rows(data)-1)' * dt;
%plot(timeline, data, filtered(:,1))

%subplot(2,1,1)
plot(timeline, data, '+;data;', 
	 timeline, k2d(:,1), '1-;kalman 2d;', 
	 timeline, k2d(:,2), '1-', 
	 timeline, k1d, '2-;kalman 1d;');
%subplot(2,1,2)
%plot(timeline, filtered(:,2), '-1');
grid()
