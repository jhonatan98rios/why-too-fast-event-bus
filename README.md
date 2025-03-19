# WhyTooFastEventBus 🚀🤔

<div align="center">
    <img src="https://github.com/jhonatan98rios/why-too-fast-event-bus/actions/workflows/tests.yml/badge.svg" alt="Tests" style="display: inline-block; margin-right: 10px;">
    <a href="https://codecov.io/gh/jhonatan98rios/why-too-fast-event-bus">
        <img src="https://codecov.io/gh/jhonatan98rios/why-too-fast-event-bus/branch/main/graph/badge.svg" alt="codecov" style="display: inline-block;">
    </a>
</div>

### "Because normal speed just isn't enough."

Welcome to WhyTooFastEventBus, the event bus that is unnecessarily fast. Do you really need this much performance? Probably not. But here we are. Whether you're making a game in PyGame or designing a complex microservices system, this absurdly fast event bus will ensure your messages arrive at speeds you never asked for.

## 🚀 Why Use This?

Blazing Fast ⚡: So fast, you'll question your life choices.

Decouples Your Code 🏗️: Because spaghetti belongs on a plate, not in your architecture.

Cross-Project Compatibility 🛠️: Works in games, backends, and anywhere Python can run.

Rust-Powered Core 🦀: Because Python wasn't fast enough for our unnecessary goals.

## 🔥 How to Use

```python
import why_too_fast_event_bus as wtf

bus = wtf.WhyTooFastEventBus()

def callback(data):
    print(f"Received: {data}")

bus.subscribe("game", "explosion", callback)

bus.publish("game", "explosion", {"boom": True})
```

Your event has now traveled at unnecessary speeds.

## 🤔 FAQ

Q: Why is this so fast?
A: Because Rust. And because we could.

Q: Do I really need an event bus this fast?
A: Probably not, but that's not the point.

Q: Can I use this in my serious production project?
A: Absolutely. Just don't tell your manager how absurdly fast it is.

## 🎉 Contributing

Want to make this even faster? Or add features we don't really need? Contributions are welcome! Check out CONTRIBUTING.md for details.
