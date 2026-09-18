# Toby Artifact layout

This file sets how to decide what a diagram shows, how to place its boxes, text, and arrows, and how to review the result. Load it for every SVG diagram, every pptx slide, and every HTML artifact that positions elements by coordinates.

## Structure

Decide what the diagram shows before you decide where anything goes.

1. Write the reader's question as one sentence. Write the diagram title as a sentence that answers it. Cut every node and arrow the answer does not need, or move it to a second diagram.
2. Pick the diagram type from the question.
   - A flowchart shows steps and choices in order.
   - A sequence diagram shows which part calls which, in time order.
   - An architecture diagram shows which parts exist and how they connect.
   - A state diagram shows the states of one thing and the events that move it between them.
   - A timeline shows when events happened. Space its events by elapsed time, or mark each gap with its length, as in `+15 min`. Even spacing draws a 1-minute gap as wide as a 15-minute gap.
3. Draw the main path as a straight line in the direction of flow. Put exceptions and exits on one side of it. At a decision, the answer that continues the main path goes straight on.
4. Put nodes that share an owner, a location, or a phase in a labelled container. The container label states the thing the nodes share, such as `repo` or `~/.claude`.
5. Give each kind of outcome one state color, and put outcomes of the same kind next to each other. A failure exit uses the consequence colors, a success exit uses the stable colors, and a report-only exit uses the info colors.
6. Write each node label so that it is true every time. Mark a part that appears only under a condition, as in `optional style, hooks`.
7. Keep every node at the same level of detail. When one node stands for a whole sub-process, draw that sub-process as its own diagram.
8. When many arrows leave one node for several targets, run them along one shared line that branches near the targets. Arrows into one node from several sources join a shared line the same way.
9. Split a diagram when it answers two questions, when one container holds more than 7 nodes, or when the arrows cannot be drawn without a crossing.

When the output is Markdown that renders Mermaid, draw a sequence diagram in Mermaid, which places the participants and messages itself.

## Plan before drawing

Write the plan as a list before you write any coordinates. The list has four parts.

1. List every node with its label text, and count the characters in the longest line of each label.
2. List every arrow as `from → to`, with its label if it has one.
3. Pick one direction of flow, either left to right or top to bottom. Every forward arrow points that way.
4. Assign each node to a grid cell by its step in the flow. Nodes at the same step share a column in a left-to-right flow, or a row in a top-to-bottom flow.

Order the nodes in each column so that the arrows between columns do not cross. When two arrows still cross, swap two nodes in one column and check again.

## Grid

Place every box, every arrow bend, and every gap on an 8px grid.

- Make each x, y, width, and height a multiple of 8. Round a size up to the next multiple of 8, never down.
- When rounding adds space to a box, split the added space evenly between opposite sides.
- On a pptx slide, one grid step is 0.0833in, which is 8px at 96 dpi.
- Stroke widths and the 2px padding tolerance in the review stay as written.
- The center of a box side falls on a 4px step when the box size is an odd multiple of 8. An arrow may attach at that point, but every bend and every shared line stays on the 8px grid.

## Text boxes

Size each box from its text. Never pick a box size first and fit the text into it afterwards.

- Budget 0.6 × the font size per character for Inter and JetBrains Mono. JetBrains Mono advances 0.6em per character. Inter averages less, so the budget leaves spare width for Inter. Budget 0.75 × the font size per character for uppercase eyebrows, because of their 0.12em tracking.
- When a browser is available, read the rendered width with `getBBox()` or `getBoundingClientRect()`, and use it in place of the budget. Measure only after every font face and weight on the page has loaded, because a width read from a fallback font sizes every box wrong.
- Box width is the widest line plus the left and right padding, rounded up to the grid. Box height is the line count × the line height, plus the top and bottom padding, rounded up to the grid.
- Use 16px padding for 13–14px text and 24px padding for 16–18px text. The top and bottom padding are equal, and the left and right padding are equal. No side has less than the set padding. Measure vertical padding from the cap height and the baseline, because the line box adds its own space above and below the letters.
- Break a label longer than 24 characters into two lines at a word boundary. SVG does not wrap text, so write each line as its own `<tspan>`.
- Center the text in its box. In SVG, set `text-anchor="middle"`, and give each line its own baseline `y` at the center of that line plus 0.35 × the font size. Leave out `dominant-baseline`, because some renderers, including QuickLook, ignore it on `<tspan>` lines and draw the text above center.
- Use a state color on a box only for that state. A decision box gets the watch colors, and a box that is not a decision never does.
- Give every box in a row the same height, and center the content of each box vertically so that its top and bottom padding stay equal. In an HTML card, use a flex column with `justify-content: center`.
- Give every box in a column the same width, so a narrower label in that column gets more left and right padding.

A label that touches no edge but sits 4px from the top and 20px from the bottom is a defect.

## Spacing

- Leave at least 24px between the outermost element and the edge of the canvas or slide.
- Leave at least 48px between grid cells that an arrow or an arrow label passes through, and at least 32px between other cells.
- Leave at least 16px between two parallel arrows.
- Keep every element inside the SVG `viewBox`, the slide bounds, or the page container.

## Arrows

- Draw each arrow as horizontal and vertical segments, with at most two bends.
- Run each arrow through the gaps between grid cells. An arrow never passes through a box or a label.
- Attach an arrow to the center of a box side. When two arrows use the same side, space their attachment points evenly along it.
- End the arrowhead 8px before the box edge, so the reader can see which box it points to.
- Route an arrow that points against the flow around the outside of the grid, and keep it to one such arrow per diagram when you can.
- Use one arrowhead and one 1.5px stroke for every arrow in the diagram.
- Place the label of a horizontal segment at the middle of the segment, on a paper-colored rectangle with the same padding rule as a text box. The segment must be at least 32px longer than the label rectangle.
- Place the label of a vertical segment 8px to the right of the line, level with the middle of the segment. Leave the line unbroken, because a label drawn across a vertical line cuts it into two short stubs.
- Keep every arrow label at least 8px from every other line and box.

## Containers

- Draw a container as a rectangle with a 12px radius, a 1px hairline border, and a `--toby-paper-2` fill.
- Put the container label at the top left as an 11px uppercase eyebrow, 16px from the top and left edges.
- Leave 24px between the container edge and its nodes, and start the nodes 16px below the label.
- Leave at least 48px between two containers, and run arrows between containers through that gap.
- Nest containers at most one level deep. A nested container uses a `--toby-paper-3` fill so that it stands out from its parent.
- An arrow crosses a container border at a right angle. An arrow never runs along a container border.

## Sequence diagrams

- Put one participant box per column at the top, sized by the text box rules.
- Space two neighbouring lifelines at least the width of the widest message label between them plus 48px.
- Draw each lifeline as a 1px dashed hairline from the bottom of its box to 24px below the last message.
- Give each message its own row, and leave 48px between rows.
- Draw a call as a solid arrow and a return as a dashed arrow.
- Center each message label 8px above its arrow.
- Draw a message from a participant to itself as a loop out to the right, 32px wide and 24px tall, with its label 8px to the right of the loop.

## Slides

- On a 16:9 pptx slide, keep all content inside a 0.5in margin on every side.
- Set the text frame insets in pptx to equal values on all four sides. The default insets are 0.1in on the left and right and 0.05in on the top and bottom.
- Turn off shrink-text-on-overflow, and size the text box for its text. Shrinking text hides the overflow and leaves a slide with mixed font sizes.
- Use no body text smaller than 12pt on a slide.
- On a slide or any canvas with a fixed size, center the diagram in the space it has. When the diagram leaves more than a quarter of the width empty, widen the gaps between its boxes.
- Size a panel or callout from its content, with the same padding rule as a text box. In a panel with left-aligned text, the left padding equals the top padding, and the right padding is at least the set padding. A panel stretched to fill the space left below a diagram fails the padding rule.

## Review

A look at the render for overlaps finds only part of the defects. Uneven padding, crowded arrow labels, and ambiguous arrow ends all pass that look. Run every step below before you describe the layout as finished.

1. Check that every SVG file parses, with `xmllint --noout`. A file that does not parse renders as an error page. XML forbids a double hyphen inside a comment, so keep flags such as `--dry-run` out of comments.
2. Render the artifact after its fonts have loaded. View it at full size, and then view each quarter of it at twice the size. A whole-page screenshot at reduced size hides a 2px overlap.
3. List every box that contains text, including nodes, panels, callouts, and slide containers, with its box coordinates, its text, and its four padding values in pixels, or in points on a pptx slide. Read each padding value from the render. A value computed from the source is only the intended value, because a renderer can place text away from its coordinates. Mark each box whose widest line exceeds its inner width. Mark each box whose top and bottom padding differ by more than 2px, or whose left and right padding differ by more than 2px. Mark each box with a side below the set padding. Mark each value that is off the 8px grid.
4. List every arrow with its start point, its bends, and its end point, and check each one on the render. Mark each arrow that crosses a box, a label, or another arrow. Mark each arrow whose end is more than 12px from the box it points to.
5. Find the element nearest each edge of the canvas, page, or slide. Mark each one that is cut off, or that is less than 24px from the edge.
6. Check the whole artifact against each rule in the Structure, Grid, Spacing, Arrows, Containers, Sequence diagrams, and Slides sections. Write down each rule that fails.
7. Fix each marked item, and repeat steps 1 to 6 on the changed parts.

When you report on the layout, give the counts from steps 3 and 4, as in `14 text boxes and 11 arrows, none marked`. The claim `there are no overflows` needs the lists from steps 3 and 4 behind it, read from the render.

When the artifact cannot be rendered in this session, say that the layout has not been verified.
