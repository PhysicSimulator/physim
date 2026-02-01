#pragma once

#include <functional>
#include <concepts>
#include <utility>
#include <type_traits>

typedef double energie;
typedef double momentum;
typedef double velocity;
typedef double mass;

template<class T>
class Unit {
protected:
  T unit{};

public:
  Unit() = default;
  explicit Unit(const T& value) : unit(value) {}

  const T& operator*() const { return unit; }
  Unit& operator=(T _unit) noexcept { 
    this->unit = std::move<T>(_unit);
    return *this;
  }

  template<class F, class... Args>
  requires  std::invocable<F, Args...> &&
            std::assignable_from<T&, std::invoke_result_t<F&, Args...>>
  Unit& operator()(F&& f, Args&&... args) {
    this->unit = std::invoke(std::forward<F>(f), std::forward<Args>(args)...);
    return *this;
  }
};

class Ekin : public Unit<energie> { 
  public:
    using Unit<energie>::Unit;
    using Unit<energie>::operator=;
    using Unit<energie>::operator*;
    using Unit<energie>::operator();
    Ekin& classical_mechanic(mass m, velocity v);
};

class Momentum : public Unit<momentum> {
public:
  using Unit<momentum>::Unit;
  using Unit<momentum>::operator=;
  using Unit<momentum>::operator*;
  using Unit<momentum>::operator();
};

class Mass : public Unit<mass> {
  using Unit<mass>::Unit;
  using Unit<mass>::operator=;
  using Unit<mass>::operator*;
  using Unit<mass>::operator();
};

class Velocity : public Unit<velocity> {
  using Unit<velocity>::Unit;
  using Unit<velocity>::operator=;
  using Unit<velocity>::operator*;
  using Unit<velocity>::operator();
};

