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

function filtered = filter_with_kalman(flt, data)
	filtered = [];
	for z = data'
		flt = kalman(flt, z);
		filtered = [filtered; flt.xhat']; % flt.xhat(2)];
	endfor
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

function filtered = with_average_velocity(data, sz, dt)
	sz = round(sz);
	filtered = [];
	for i = 1:rows(data);
		s = data(i);
		if (i <= sz)
			sminus = data(1);
		else
			sminus = data(i - sz);
		endif
		ds = s - sminus;
		v = ds / (sz * dt);
		filtered = [filtered;s v];
	endfor
endfunction

function filtered = test_kalman_2d(data, dt, q, r, x0)
	Q = [(dt^4)/4, (dt^3)/2; (dt^3)/2, dt^2] * q;  % process covariance
	R = r;  % measurement covarience
	A = [1, dt; 0, 1];
	H = [1, 0];

	% Initial state
	xhat = [x0; 0];
	P = Q * 100;

	flt = make_kalman(Q, R, A, H, xhat, P);
	filtered = filter_with_kalman(flt, data);
endfunction

function filtered = test_kalman_1d(data, dt, q, r, x0)
	Q = dt^2 / 2 * q;
	R = r;
	A = 1;
	H = 1;
	xhat = x0;
	P = Q;

	flt = make_kalman(Q, R, A, H, xhat, P);
	filtered = filter_with_kalman(flt, data);
endfunction

function filtered = test_movavg(data, sz)
	filtered = [];
	samples = [];
	for s = data'
		samples = [samples s];
		if (columns(samples) > sz);
			samples = samples(2:columns(samples));
		endif

		filtered = [filtered; mean(samples)];
	endfor
endfunction

function filtered = test_alphabeta(data, dt, a, b, x0)
	x = xminus = x0;
	v = vminus = 0;
	filtered = [];
	for xm = data'
		x = xminus + vminus * dt;
		v = vminus;

		r = xm - x;
        x += a * r;
		v += b * r / dt;

		xminus = x;
		vminus = v;

		filtered = [filtered; x v];
	endfor
endfunction

% Load data
% load altchange.mat
load data.mat
datarate = 1/dt

%data = normal_rnd(mean(data), var(data), rows(data), 1);


data = pressure_to_alt(data);
% Basic filter for KDR vario sampled data

%dt = 1/16;
q = 0.400;  % process variance
r = .50;   % measurement variance
x0 = mean(data)

% perform tests
k2d = test_kalman_2d(data, dt, q, r, x0);
k1d = test_kalman_1d(data, dt, q, r, x0);
movavg = test_movavg(data, 2.7/dt);	
ab = test_alphabeta(data, dt, 0.08, 0.0033, x0);

% add average velocity
k1d = with_average_velocity(k1d, 1/dt, dt);
movavg = with_average_velocity(movavg, 1/dt, dt);

% plot data
timeline = (0:rows(data)-1)' * dt;


% display statistics
disp("Data variance"), disp(var(data))
disp("Variance kalman 2d"), disp(var(k2d))
disp("Variance kalman 1d"), disp(var(k1d))
disp("Variance moving average"), disp(var(movavg))

%subplot(2,1,1)

figure(1, 'position',[0, 0, 1000, 650]);
plot(timeline, data, '0+;data;', 
	 timeline, k2d(:,1), '1-;kalman 2d;', 
	 %timeline, k2d(:,2), '1-', 
	 %timeline, k1d(:,1), '2-;kalman 1d;',
	 timeline, ab(:,1), '2-;alpha-beta;',
	 timeline, movavg(:,1), '3-;moving avg;');
grid();
xlabel("Time (s)");
ylabel("Altitude (m)");
title("Altitude estimation");

%subplot(2,1,2)
figure(2);
plot(timeline, k2d(:,2), '1-;kalman 2d;',
	 %timeline, k1d(:,2), '2-;kalman 1d;',
	 timeline, ab(:,2), '2-;alpha-beta;',
	 timeline, movavg(:,2), '3-;moving avg;');
grid();
xlabel("Time (s)")
ylabel("Vertical speed (m/s)");
title("Vertical speed estimation")
pause;
