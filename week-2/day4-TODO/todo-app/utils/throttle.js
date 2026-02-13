export function throttle(fn, limit) {
  let waiting = false;

  return function (...args) {
    if (!waiting) {
      fn.apply(this, args);
      waiting = true;

      setTimeout(() => waiting = false, limit);
    }
  };
}
